import requests

def scan_sqli(target_url):
    payloads = ["'", "' OR '1'='1", "1' OR '1'='1' --", "\" OR \"1\"=\"1"]
    error_signs = ["sql syntax", "mysql", "syntax error", "unclosed quotation", "sqlite", "odbc"]

    results = []
    vulnerable = False

    for payload in payloads:
        try:
            test_url = target_url + payload
            response = requests.get(test_url, timeout=5)
            content = response.text.lower()
            found_error = any(sign in content for sign in error_signs)
            if found_error:
                vulnerable = True
                results.append({"payload": payload, "status": "VULNERABLE ⚠️"})
            else:
                results.append({"payload": payload, "status": "Safe"})
        except requests.exceptions.RequestException:
            results.append({"payload": payload, "status": "Could not test (connection error)"})

    return {"vulnerable": vulnerable, "tests": results}