import re
import os
import hashlib
from flask import Flask, render_template, request, send_file, session, redirect, url_for, flash
from scanner.port_scanner import scan_ports
from scanner.sqli_scanner import scan_sqli
from scanner.xss_scanner import scan_xss
from scanner.header_scanner import scan_headers
from scanner.ssl_checker import check_ssl
from scanner.password_checker import check_password
from scanner.report_generator import generate_pdf_report
from scanner.ai_suggester import suggest_strong_password
from database import init_db, add_user, get_user, save_scan, get_scan_history

app = Flask(__name__)
app.secret_key = 'tamizhan_security_2024_secret'

init_db()

last_scan_data = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_url(url):
    pattern = re.compile(r'^(https?:\/\/)?([\da-zA-Z\.-]+)\.([a-zA-Z\.]{2,6})([\/\w \.-]*)*\/?$')
    return re.match(pattern, url) is not None

def calculate_risk_score(ports, sqli, xss, headers, ssl):
    score = 100
    score -= len(ports.get('open_ports', [])) * 5
    if sqli.get('vulnerable'):
        score -= 25
    if xss.get('vulnerable'):
        score -= 20
    missing_headers = [h for h in headers.get('results', []) if h['status'] == 'Missing ⚠️']
    score -= len(missing_headers) * 5
    if not ssl.get('valid'):
        score -= 15
    score = max(0, min(100, score))
    if score >= 80:
        grade = "🟢 Low Risk"
    elif score >= 50:
        grade = "🟡 Medium Risk"
    else:
        grade = "🔴 High Risk"
    return {"score": score, "grade": grade}

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session.get('username'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if not username or not email or not password:
            flash('All fields are required!', 'danger')
            return render_template('register.html')
        hashed = hash_password(password)
        if add_user(username, hashed, email):
            flash('Account created! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username or email already exists!', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed = hash_password(password)
        user = get_user(username)
        if user and user[2] == hashed:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/scan', methods=['POST'])
def scan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    global last_scan_data
    target_url = request.form.get('target_url')
    if not target_url or not is_valid_url(target_url):
        return render_template('error.html', message="❌ Invalid URL.")
    if not target_url.startswith("http"):
        target_url = "https://" + target_url
    clean_target = target_url.replace("https://", "").replace("http://", "").split('/')[0]
    port_results = scan_ports(clean_target)
    sqli_results = scan_sqli(target_url)
    xss_results = scan_xss(target_url)
    header_results = scan_headers(target_url)
    ssl_results = check_ssl(clean_target)
    risk = calculate_risk_score(port_results, sqli_results, xss_results, header_results, ssl_results)
    last_scan_data = {
        "target": target_url,
        "ports": port_results,
        "sqli": sqli_results,
        "xss": xss_results,
        "headers": header_results,
        "ssl": ssl_results,                                                                                                                                                                                                                                            
        "risk": risk
    }
    save_scan(
        session['user_id'], target_url,
        risk['score'], risk['grade'],
        len(port_results.get('open_ports', [])),
        1 if sqli_results.get('vulnerable') else 0,
        1 if xss_results.get('vulnerable') else 0,
        1 if ssl_results.get('valid') else 0
    )
    return render_template('result.html', target=target_url, ports=port_results,
                           sqli=sqli_results, xss=xss_results, headers=header_results,
                           ssl=ssl_results, risk=risk, username=session.get('username'))

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    scans = get_scan_history(session['user_id'])
    return render_template('history.html', scans=scans, username=session.get('username'))

@app.route('/download-report')
def download_report():
    if not last_scan_data:
        return "No scan data available. Please run a scan first.", 400
    try:
        path = generate_pdf_report(last_scan_data)
        return send_file(path, as_attachment=True, download_name="scan_report.pdf")
    except Exception as e:
        return f"Error generating report: {str(e)}", 500

@app.route('/password-check', methods=['GET', 'POST'])
def password_check():
    result = None
    ai_suggestion = None
    if request.method == 'POST':
        pwd = request.form.get('password')
        result = check_password(pwd)
        if result['strength'] in ['Weak', 'Medium']:
            ai_suggestion = suggest_strong_password(pwd)
    return render_template('password.html', result=result, ai_suggestion=ai_suggestion)

if __name__ == '__main__':
    app.run(debug=True)  