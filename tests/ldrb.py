from asm import *

def prog():
    movi( r0, 0x1000 )
    movi( r1, 9 )
    strb( r1, r0 )
    ldrb( r2, r0 )
    halt()


assemble(prog, 0x100)

save()

