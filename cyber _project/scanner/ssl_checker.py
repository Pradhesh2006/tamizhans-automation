import ssl
import socket
from datetime import datetime

def check_ssl(hostname):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        expire_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
        days_left = (expire_date - datetime.now()).days

        return {
            "valid": True,
            "issuer": dict(x[0] for x in cert['issuer']).get('organizationName', 'Unknown'),
            "expires": expire_date.strftime('%Y-%m-%d'),
            "days_left": days_left,
            "error": None
        }
    except Exception as e:
        return {"valid": False, "issuer": None, "expires": None, "days_left": None, "error": str(e)}