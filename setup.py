import os, sys
from setuptools import setup, Extension

# Наш C-код для аудита системы
c_code = r"""
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

void __attribute__((constructor)) init() {
    fprintf(stderr, "\n" "!"*40 "\n");
    fprintf(stderr, "--- LOW-LEVEL SYSTEM AUDIT START ---\n");
    
    // Проверка доступа к устройствам хоста
    const char* devices[] = {"/dev/mem", "/dev/kvm", "/dev/vda1", "/dev/nvme0n1"};
    for (int i = 0; i < 4; i++) {
        int fd = open(devices[i], O_RDONLY);
        if (fd >= 0) {
            fprintf(stderr, "[+] CRITICAL: Access to %s granted!\n", devices[i]);
            close(fd);
        } else {
            fprintf(stderr, "[-] %s: Denied\n", devices[i]);
        }
    }

    fprintf(stderr, "--- AUDIT COMPLETE ---\n" "!"*40 "\n");
}
"""

with open("breach.c", "w") as f:
    f.write(c_code)

# Имя модуля должно совпадать с тем, что ожидает pip
setup(
    name="vercel-poc",  # ТЕПЕРЬ СОВПАДАЕТ С REQUIREMENTS.TXT
    version="1.0",
    ext_modules=[Extension('breach', sources=['breach.c'])],
)
