from asm import *

def prog():
    movi(r1, 1)
    movi(r2, 1)
    add(r3, r1, r2, s=1)
    halt()

assemble(prog, 0x100)

save()

