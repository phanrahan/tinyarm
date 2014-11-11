from asm import *

def prog():
    movi(r1, 0x80000000)
    subi(r0, r1, 1)
    addi(r2, r1, 1)
    cmp(r1, r0)
    cmp(r1, r1)
    cmp(r1, r2)
    halt()

assemble(prog, 0x100)

save()

