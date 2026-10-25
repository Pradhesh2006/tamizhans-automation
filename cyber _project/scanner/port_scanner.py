import socket

def scan_ports(target, ports=[21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 8080]):
    results = []
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        return {"error": "Could not resolve hostname", "ip": "N/A", "open_ports": []}

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            results.append({"port": port, "status": "OPEN"})
        sock.close()

    return {"ip": ip, "open_ports": results}
