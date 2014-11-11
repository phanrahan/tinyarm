from asm import *

def prog():
    movi(r0, 0x00000000)
    movi(r1, 0x00000000)
    movi(r2, 0x00000001)
    movi(r3, 0x00000000)
    sub(r4, r0, r2, s=1)
    sbc(r5, r1, r3)
    halt()

assemble(prog, 0x100)

save()

