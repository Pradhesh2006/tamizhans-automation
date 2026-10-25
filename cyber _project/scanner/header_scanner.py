import requests

def scan_headers(target_url):
    important_headers = {
        "Content-Security-Policy": "Prevents XSS and injection attacks",
        "X-Frame-Options": "Prevents clickjacking",
        "X-Content-Type-Options": "Prevents MIME-sniffing attacks",
        "Strict-Transport-Security": "Forces HTTPS connections",
        "X-XSS-Protection": "Browser XSS filter"
    }

    results = []
    try:
        response = requests.get(target_url, timeout=5)
        headers = response.headers
        for header, purpose in important_headers.items():
            if header in headers:
                results.append({"header": header, "status": "Present ✅", "purpose": purpose})
            else:
                results.append({"header": header, "status": "Missing ⚠️", "purpose": purpose})
        return {"results": results, "error": None}
    except requests.exceptions.RequestException:
        return {"results": [], "error": "Could not connect to target"} 