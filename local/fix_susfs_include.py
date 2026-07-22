#!/usr/bin/env python3
# Fixup: ensure <linux/susfs_def.h> is included in files the SUSFS patch
# touched, in case the patch's include hunk failed on the OnePlus source.
import os

FILES = ['./fs/proc/base.c', './fs/proc/task_mmu.c']

INC = (
    '#if defined(CONFIG_KSU_SUSFS_SUS_MAP) || defined(CONFIG_KSU_SUSFS_OPEN_REDIRECT)\n'
    '#include <linux/susfs_def.h>\n'
    '#endif\n'
)
MARKER = '#include <linux/cpufreq_times.h>'

for fn in FILES:
    if not os.path.exists(fn):
        print('SKIP', fn, '(not found)')
        continue
    with open(fn) as f:
        c = f.read()
    if '#include <linux/susfs_def.h>' in c:
        print('OK  ', fn, '(already includes susfs_def.h)')
        continue
    if MARKER in c:
        c = c.replace(MARKER, MARKER + '\n' + INC, 1)
    else:
        # fallback: insert after the last top-of-file #include <linux/...>
        idx = c.rfind('#include <linux/')
        nl = c.find('\n', idx)
        c = c[:nl + 1] + INC + c[nl + 1:]
    with open(fn, 'w') as f:
        f.write(c)
    print('FIX ', fn, '(added susfs_def.h include)')
