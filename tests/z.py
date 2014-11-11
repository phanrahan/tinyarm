from asm import *

def prog():
    movi(r1, 1)
    tsti(r1, 1)
    tsti(r1, 2)
    teqi(r1, 1)
    teqi(r1, 2)
    halt()

assemble(prog, 0x100)

save()

