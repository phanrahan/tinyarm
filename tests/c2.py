from asm import *

def prog():
    movi(r0, 0x80000000 )

    movi(r1, 0x80000000 )
    subi(r1, r1, 1 )
    sub(r2, r0, r1, s=1 )

    movi(r1, 0x80000000 )
    sub(r2, r0, r1, s=1 )

    movi(r1, 0x80000000 )
    addi(r1, r1, 1 )
    sub(r2, r0, r1, s=1 )

    halt()

assemble(prog, 0x100)

save()

