from asm import *

def prog():
    movi(r0, 0x80000000)
    movi(r1, 0x00000000)
    movi(r2, 0x80000000)
    movi(r3, 0x00000000)
    add(r4, r0, r2, s=1)
    adc(r5, r1, r3)
    halt()

assemble(prog, 0x100)

save()

