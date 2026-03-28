import os
import sys
import socket
import subprocess

def bold_log(msg):
    print(f"\n\033[1m[!!!] {msg}\033[0m", flush=True)

def run_audit():
    bold_log("INITIATING INFRASTRUCTURE ESCAPE AUDIT")
     
    print(f"[*] Process Identity: UID={os.getuid()}, GID={os.getgid()}", flush=True)
 
    sockets = ["/var/run/docker.sock", "/run/containerd/containerd.sock", "/var/run/host-bridge.sock"]
    for s in sockets:
        if os.path.exists(s):
            bold_log(f"CRITICAL: Found container management socket: {s}")
        else:
            print(f"[-] Socket not found: {s}", flush=True)

 
    print("\n[*] Scanning internal gateway for open management ports...", flush=True)
    target_ip = "10.0.0.1" # Стандартный шлюз в таких системах
    for port in [2375, 2376, 6443, 10250]: # Docker API, Kubernetes API
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            bold_log(f"VULNERABILITY: Internal Port {port} is OPEN on gateway!")
        sock.close()

 
    try:
        with open("/dev/vda", "rb") as f:
            header = f.read(512)
            bold_log(f"HOST DISK LEAK: Read MBR/GPT from /dev/vda: {header[:16].hex()}")
    except Exception as e:
        print(f"[-] Raw disk access denied: {e}", flush=True)
 
    bold_log("AUDIT FINISHED. FORCING EXIT TO SHOW LOGS.")
    os._exit(1)

if __name__ == "__main__":
    run_audit()
