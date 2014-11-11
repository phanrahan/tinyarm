from asm import *

def prog():
    movi( r0, 0x20000000 )
    movi( r1, 1 )
    str( r1, r0, 0x04, post=1 )
    str( r1, r0, 0x04, post=1 )
    halt()


assemble(prog, 0x100)

save()

