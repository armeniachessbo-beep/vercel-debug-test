import os, sys, subprocess

def log_bold(msg):
    print(f"\n{'='*60}\n[!] {msg}\n{'='*60}", flush=True)

def crash_and_burn():
    log_bold("STARTING CRITICAL INFRASTRUCTURE AUDIT")

    
    uid = os.getuid()
    log_bold(f"CURRENT IDENTITY: UID={uid} ({'ROOT' if uid==0 else 'USER'})")

     
    print("[*] Attempting to leak PID 1 Environment Variables...", flush=True)
    try:
        with open('/proc/1/environ', 'rb') as f:
            data = f.read().replace(b'\0', b'\n').decode(errors='ignore')
            for line in data.split('\n'):
                if line:
                     
                    key = line.split('=')[0]
                    print(f"    LEAKED KEY: {key}", flush=True)
    except Exception as e:
        print(f"    [-] PID 1 access denied: {e}", flush=True)

     
    print("\n[*] Testing Raw Socket capabilities (Network Sniffing)...", flush=True)
    try:
        import socket
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, 0x0003)
        log_bold("CRITICAL: RAW SOCKETS ENABLED! MitM possible.")
        s.close()
    except Exception as e:
        print(f"    [-] Raw sockets restricted: {e}", flush=True)

    
    print("\n[*] Searching for Service Account Tokens...", flush=True)
    token_path = "/var/run/secrets/kubernetes.io/serviceaccount/token"
    if os.path.exists(token_path):
        log_bold(f"FOUND K8S TOKEN: {token_path}")
    else:
        print("    [-] No K8S tokens found in standard path.", flush=True)

   
    log_bold("AUDIT COMPLETE. FORCING BUILD FAILURE TO SHOW LOGS.")
    sys.exit(1)

if __name__ == "__main__":
    crash_and_burn()
