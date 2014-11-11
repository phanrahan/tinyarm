from asm import *

def prog():
    movi(r1, 1)
    subi(r0, r1, 0, s=1)
    subi(r0, r1, 1, s=1)
    subi(r0, r1, 2, s=1)
    halt()

assemble(prog, 0x100)

save()

