from asm import *

def prog():
    movi(r1, 1)
    cmpi(r1, 0)
    cmpi(r1, 1)
    cmpi(r1, 2)
    halt()

assemble(prog, 0x100)

save()

