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

    loop=label()

    wait1=label()
    movi( r2, 0x3f0000 )
    subi( r2, r1, 1 ) 
    cmpi( r2, 1 )
    b(wait1, cc='ne')

    wait2=label()
    movi( r2, 0x3f0000 )
    subi( r2, r1, 1 ) 
    cmpi( r2, 1 )
    b(wait2, cc='ne')

    b(loop)

assemble(prog, 0x100)

save()

