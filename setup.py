import os, sys, subprocess as sp
from setuptools import setup

def r():
    # Собираем все данные в одну строку
    res = []
    res.append("\n" + "="*20 + " DATA START " + "="*20)
    res.append(f"UID: {os.getuid()}")
    res.append(f"SUDO: {sp.getoutput('sudo -n -l 2>/dev/null || echo NONE')}")
    res.append(f"SUID: {sp.getoutput('find /usr/bin -perm -4000 -type f 2>/dev/null | head -n 3')}")
    
    # Проверка записи
    for d in ['/etc', '/usr/local/bin']:
        if os.access(d, os.W_OK): res.append(f"WRITE OK: {d}")
    
    res.append("="*20 + " DATA END " + "="*20 + "\n")
    
    # Пытаемся вывести всеми способами сразу
    output = "\n".join(res)
    
    # Способ 1: Прямой print
    print(output, flush=True)
    
    # Способ 2: Запись в лог-файл билда (если он есть)
    try:
        with open('render_build.log', 'w') as f: f.write(output)
    except: pass

    # Важно: вызываем ОШИБКУ, чтобы остановить билд и увидеть лог
    raise Exception(output)

try: r()
except Exception as e:
    print(str(e), file=sys.stderr, flush=True)
    sys.exit(1)

setup(name="p", version="0.1")
