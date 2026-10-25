<<<<<<< HEAD
# Tamizhan's Security Automation

A Flask-based web application for basic security checks on websites you own or are authorized to assess. It combines a small set of website checks with account-based scan history and a password-strength page.

## Features

- User registration, login, and logout
- Website checks for:
  - Common TCP ports
  - Indicators of SQL injection and reflected cross-site scripting (XSS)
  - Selected HTTP security headers
  - TLS/SSL certificate validity and expiry
- A simple risk score based on scan results
- Per-account scan history stored in SQLite
- Downloadable PDF scan reports
- Password strength feedback, breach lookup through the Pwned Passwords range API, and locally generated password suggestions

These checks are basic indicators, not a comprehensive security assessment. A result marked safe does not prove that a site is secure.

## Requirements

- Python 3.10 or later
- pip
- Network access for target checks and the optional password breach lookup

Dependencies are pinned in [`requirements.txt`](requirements.txt).

## Setup

From this project directory, create and activate a virtual environment, then install the dependencies.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the application

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. Register an account, sign in, enter an authorized target URL, and start a scan. The home page also links to scan history and the password checker.

The app initializes the SQLite database (`users.db`) when it starts. Scan reports can be downloaded after a scan using the report link on the results page.

## Project layout

```text
app.py                    Flask routes and scan orchestration
database.py               SQLite setup and persistence functions
scanner/                  Website checks, password checks, and PDF reporting
templates/                Jinja HTML pages
static/                   CSS, JavaScript, and static assets
requirements.txt          Python dependencies
users.db                  SQLite database (created/updated by the app)
```

## Important security notes

- Only scan systems for which you have explicit authorization. Scans make network requests to the supplied host and test common ports.
- The password breach check sends only the first five characters of the password's SHA-1 hash to the Pwned Passwords range API; the full password is not sent by that lookup. Avoid entering passwords you currently use on sensitive accounts into a demo application.
- This project is configured for local development: `app.py` uses Flask's development server with debug mode enabled and a hard-coded session secret. Do not expose it to the public internet or use it as-is in production. Before deployment, disable debug mode, configure a strong secret outside source control, and review authentication and password storage.
=======
# tamizhans-automation
>>>>>>> 0d52070ab4aacf86d01f873d5aa34e833eb08667
