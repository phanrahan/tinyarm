from asm import *

def prog():
    movi(r1, 1)
    movi(r2, 2)
    movi(r3, 3)

    and_(r0, r1, r1)
    eor(r0, r1, r1)
    sub(r0, r1, 1)
    rsb(r0, r1, r1)
    add(r0, r1, r1)
    adc(r0, r1, r1)
    sbc(r0, r1, r1)
    rsc(r0, r1, r1)
    tst(r1, r1)
    teq(r1, r1)
    cmp(r1, r1)
    cmn(r1, r1)
    orr(r0, r1, r1)
    mov(r0, r1)
    bic(r0, r1, r1)
    mvn(r0, r1)

    halt()

assemble(prog, 0x100)

save()

