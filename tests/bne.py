
from asm import *

def prog():
    movi(r0, 2)
    loop = label()
    subi(r0, r0, 1, s=1)
    b(loop, cc='ne')
    halt()

assemble(prog, 0x100)

save()

