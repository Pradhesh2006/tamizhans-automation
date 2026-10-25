import re
import hashlib
import requests

def check_password(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Too short (use 8+ characters)")

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add an uppercase letter")

    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add a lowercase letter")

    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("Add a number")

    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("Add a special character")

    strength = "Weak"
    if score >= 4:
        strength = "Strong"
    elif score >= 2:
        strength = "Medium"

    breach_count = check_breach(password)

    return {"strength": strength, "score": score, "feedback": feedback, "breach_count": breach_count}

def check_breach(password):
    try:
        sha1pwd = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = sha1pwd[:5], sha1pwd[5:]
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=5)
        for line in response.text.splitlines():
            hash_suffix, count = line.split(':')
            if hash_suffix == suffix:
                return int(count)
        return 0
    except Exception:
        return -1                                                                                    