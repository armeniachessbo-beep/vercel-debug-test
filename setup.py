import os
import subprocess

def demonstrate_impact():
    print("--- BUG BOUNTY PROOF OF CONCEPT ---")
    
    # 1. Показываем, что мы в контейнере и имеем доступ к сети
    # Вместо кражи ключей, просто проверяем доступность эндпоинта
    print(f"Hostname: {subprocess.getoutput('hostname')}")
    
    # 2. Демонстрируем доступ к переменным окружения (без вывода секретов полностью)
    # Это доказывает, что ты можешь читать конфиги.
    env_keys = [k for k in os.environ.keys() if "VERCEL" in k or "TOKEN" in k]
    print(f"Accessible sensitive ENV keys: {env_keys}")

    # 3. Проверка привилегий (Docker Escape Hint)
    # Если ты можешь прочитать список процессов хоста - это уже Critical.
    try:
        if os.path.exists("/sys/fs/cgroup/cgroup.procs"):
            print("[CONFIRMED] Cgroup v2 access available - Potential Container Escape.")
    except:
        pass

    print("--- END OF POC ---")

# demonstrate_impact()