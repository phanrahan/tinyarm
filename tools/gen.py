import sys
from arch import Arch

if len(sys.argv) != 2:
    print 'usage: python asm.py proc.arch > proc.mas'
    sys.exit(1)

lines = open(sys.argv[1]).readlines()
arch = Arch(lines)


