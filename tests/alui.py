from asm import *

def prog():
    movi(r1, 1)
    movi(r2, 2)
    movi(r3, 3)

    andi(r0, r1, 1)
    eori(r0, r1, 1)
    subi(r0, r1, 1)
    rsbi(r0, r1, 1)
    addi(r0, r1, 1)
    adci(r0, r1, 1)
    sbci(r0, r1, 1)
    rsci(r0, r1, 1)
    tsti(r1, 1)
    teqi(r1, 1)
    cmpi(r1, 1)
    cmni(r1, 1)
    orri(r0, r1, 1)
    movi(r0, 1)
    bici(r0, r1, 1)
    mvni(r0, 1)

    halt()

assemble(prog, 0x100)

save()

