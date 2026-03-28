import os, sys
print("\n" + "="*40)
print(f"IDENTITY: UID={os.getuid()} GID={os.getgid()}")
try:
    with open('/proc/1/environ', 'rb') as f:
        print("SENSITIVE: Proc 1 Environ Access Granted")
except:
    print("SENSITIVE: Proc 1 Access Denied")
print("="*40 + "\n")
# Вызываем ошибку, чтобы деплой СДОХ и показал логи
sys.exit(1)
