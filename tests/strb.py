from asm import *

def prog():
    movi( r0, 0x20000000 )
    movi( r1, 1 )
    strb( r1, r0 )
    halt()


assemble(prog, 0x100)

save()

