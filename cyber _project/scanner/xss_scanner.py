import requests

def scan_xss(target_url):
    payloads = ["<script>alert(1)</script>", "\"><script>alert(1)</script>", "<img src=x onerror=alert(1)>"]
    results = []
    vulnerable = False

    for payload in payloads:
        try:
            test_url = target_url + payload
            response = requests.get(test_url, timeout=5)
            if payload in response.text:
                vulnerable = True
                results.append({"payload": payload, "status": "VULNERABLE ⚠️"})
            else:
                results.append({"payload": payload, "status": "Safe"})
        except requests.exceptions.RequestException:
            results.append({"payload": payload, "status": "Could not test (connection error)"})

    return {"vulnerable": vulnerable, "tests": results}