from asm import *

def prog():
    movi( r0, 0x20000000 )
    movi( r1, 0x00200000 )
    orr( r0, r0, r1 )

    movi( r1, 1 )
    lsl( r1, 3 )
    str( r1, r0, 0x08 )

    movi( r1, 1 )
    lsl( r1, 21 )
    str( r1, r0, 0x1c )

    halt()


assemble(prog, 0x100)

save()

