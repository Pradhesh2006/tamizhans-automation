import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS scan_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        target_url TEXT NOT NULL,
        risk_score INTEGER,
        risk_grade TEXT,
        port_count INTEGER,
        sqli_vulnerable INTEGER,
        xss_vulnerable INTEGER,
        ssl_valid INTEGER,
        scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    conn.commit()
    conn.close()

def add_user(username, password, email):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                  (username, password, email))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_user(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def save_scan(user_id, target_url, risk_score, risk_grade, port_count, sqli_vulnerable, xss_vulnerable, ssl_valid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO scan_history 
        (user_id, target_url, risk_score, risk_grade, port_count, sqli_vulnerable, xss_vulnerable, ssl_valid)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (user_id, target_url, risk_score, risk_grade, port_count, sqli_vulnerable, xss_vulnerable, ssl_valid))
    conn.commit()
    conn.close()

def get_scan_history(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM scan_history WHERE user_id = ? ORDER BY scanned_at DESC", (user_id,))
    history = c.fetchall()
    conn.close()
    return history