from asm import *

def prog():
    movi(r1, 0xfff)
    halt()

assemble(prog, 0x100)

save()

