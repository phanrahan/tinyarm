from asm import *

def prog():
    movi(r1,1)
    mov(r0, r1, shift=1)

    halt()

assemble(prog, 0x100)

save()

