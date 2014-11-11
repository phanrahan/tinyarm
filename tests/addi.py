from asm import *

def prog():
    movi(r1, 1)
    addi(r2, r1, 1)
    adci(r3, r1, 1)
    subi(r4, r1, 1)
    sbci(r5, r1, 1)
    rsbi(r6, r1, 1)
    rsci(r7, r1, 1)
    loop = label()
    b(loop)

assemble(prog, 0x100)

save()

