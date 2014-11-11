from asm import *

delay = 0

def prog():
    global delay
    movi(r0, 0x1)
    bl(delay)
    movi(r0, 0x3)
    movi(r0, 0x4)
    halt()
    delay = label()
    movi(r0, 0x2)
    bx(lr)

assemble(prog, 0x100)

save()

