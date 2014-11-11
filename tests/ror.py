from asm import *

def prog():
    movi(r0, 3)
    ror(r0, shift=1)
    halt()

assemble(prog, 0x100)

save()

