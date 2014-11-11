from arch import Arch
from bits import rol
from tinyasm import *

# registers
r0 = 0
r1 = 1
r2 = 2
r3 = 3
r4 = 4
r5 = 5
r6 = 6
r7 = 7
r8 = 8
r9 = 9
r10 = 10
r11 = 11
r12 = 12
r13 = 13
r14 = 14
r15 = 15

sp = r13
lr = r14
pc = r15

arch = Arch('arm.arch')

# alu register shift immediate
def aluri(op, ra, rb, rc, shift, shifttype, s, cc):
    f = arch.table['f'].index(cc)
    h = arch.table['h'].index(shifttype)
    q = arch.table['q'].index(op)
    inst = arch.match(0x00000000)
    args = dict( q=q, a=ra, b=rb, c=rc, u=shift, h=h, f=f, s=s )
    emit( inst.encode(args, getpc()) )

# alu register shift register
def alurr(op, ra, rb, rc, rd, shifttype, s, cc):
    f = arch.table['f'].index(cc)
    h = arch.table['h'].index(shifttype)
    q = arch.table['q'].index(op)
    inst = arch.match(0x00000010)
    args = dict( q=q, a=ra, b=rb, c=rc, d=rd, h=h, f=f, s=s )
    emit( inst.encode(args, getpc()) )

def rotation(u):
    org = u
    rot = 0
    for i in range(16):
        if (u & ~0xff) == 0:
            return u, rot
        u = rol( u, 2 )
        rot += 1

    print 'Immediate value requires more than 8-bits: %08x' % org
    return org & 0xff, 0

def alui(op, ra, rb, u, s, cc):
    assert u >= 0
    f = arch.table['f'].index(cc)
    q = arch.table['q'].index(op)
    u, i = rotation(u)
    inst = arch.match(0x02000000)
    args = dict( q=q, a=ra, b=rb, u=u, i=i, f=f, s=s )
    emit( inst.encode(args, getpc()) )


# data operations register shifted immediate

def and_(ra, rb, rc, shift=0, shifttype='LSL', s=0, cc=''):
    aluri("and", ra, rb, rc, shift, shifttype, s, cc)

def eor(ra, rb, rc, shift=0, shifttype='LSL', s=0, cc=''):
    aluri("eor", ra, rb, rc, shift, shifttype, s, cc)

def sub(ra, rb, rc, shift=0, shifttype='LSL', s=0, cc=''):
    aluri("sub", ra, rb, rc, shift, shifttype, s, cc)

def rsb(ra, rb, rc, shift=0, shifttype='LSL', s=0, cc=''):
    aluri("rsb", ra, rb, rc, shift, shifttype, s, cc)

def add(ra, rb, rc, shift=0, shifttype='LSL', s=0, cc=''):
    aluri("add", ra, rb, rc, shift, shifttype, s, cc)

def adc(ra, rb, rc, shift=0, shifttype='LSL', s=0, cc=''):
    aluri("adc", ra, rb, rc, shift, shifttype, s, cc)

def sbc(ra, rb, rc, shift=0, shifttype='LSL', s=0, cc=''):
    aluri("sbc", ra, rb, rc, shift, shifttype, s, cc)

def rsc(ra, rb, rc, shift=0, shifttype='LSL', s=0, cc=''):
    aluri("rsc", ra, rb, rc, shift, shifttype, s, cc)

def tst(ra, rb, shift=0, shifttype='LSL', cc=''):
    aluri("tst", ra, 0, rb, shift, shifttype, 1, cc)

def teq(ra, rb, shift=0, shifttype='LSL', cc=''):
    aluri("teq", ra, 0, rb, shift, shifttype, 1, cc)

def cmp(ra, rb, shift=0, shifttype='LSL', cc=''):
    aluri("cmp", ra, 0, rb, shift, shifttype, 1, cc)

def cmn(ra, rb, shift=0, shifttype='LSL', cc=''):
    aluri("cmn", ra, 0, rb, shift, shifttype, 1, cc)

def orr(ra, rb, rc, shift=0, shifttype='LSL', s=0, cc=''):
    aluri("orr", ra, rb, rc, shift, shifttype, s, cc)

def mov(ra, rb, shift=0, shifttype='LSL', s=0, cc=''):
    aluri("mov", ra, 0, rb, shift, shifttype, s, cc)

def bic(ra, rb, rc, shift=0, shifttype='LSL', s=0, cc=''):
    aluri("bic", ra, rb, rc, shift, shifttype, s, cc)

def mvn(ra, rb, shift=0, shifttype='LSL', s=0, cc=''):
    aluri("mvn", ra, 0, rb, shift, shifttype, s, cc)


# data operations immediate

def andi(ra, rb, imm, s=0, cc=''):
    alui("and", ra, rb, imm, s, cc)

def eori(ra, rb, imm, s=0, cc=''):
    alui("eor", ra, rb, imm, s, cc)

def subi(ra, rb, imm, s=0, cc=''):
    alui("sub", ra, rb, imm, s, cc)

def rsbi(ra, rb, imm, s=0, cc=''):
    alui("rsb", ra, rb, imm, s, cc)

def addi(ra, rb, imm, s=0, cc=''):
    alui("add", ra, rb, imm, s, cc)

def adci(ra, rb, imm, s=0, cc=''):
    alui("adc", ra, rb, imm, s, cc)

def sbci(ra, rb, imm, s=0, cc=''):
    alui("sbc", ra, rb, imm, s, cc)

def rsci(ra, rb, imm, s=0, cc=''):
    alui("rsc", ra, rb, imm, s, cc)

def tsti(ra, imm, cc=''):
    alui("tst", ra, 0, imm, 1, cc)

def teqi(ra, imm, cc=''):
    alui("teq", ra, 0, imm, 1, cc)

def cmpi(ra, imm, cc=''):
    alui("cmp", ra, 0, imm, 1, cc)

def cmni(ra, imm, cc=''):
    alui("cmn", ra, 0, imm, 1, cc)

def orri(ra, rb, imm, s=0, cc=''):
    alui("orr", ra, rb, imm, s, cc)

def movi(ra, imm, s=0, cc=''):
    alui("mov", ra, 0, imm, s, cc)

def bici(ra, rb, imm, s=0, cc=''):
    alui("bic", ra, rb, imm, s, cc)

def mvni(ra, imm, s=0, cc=''):
    alui("mvn", ra, 0, imm, s, cc)

# load/store instructions

def ldsr( load, byte, ra, rb, u, pre, post, cc ):
    f = arch.table['f'].index(cc)

    p = 1 # pre by default
    t = 0
    if pre or post:
        t=1 # write-back
        if post:
            p = 0


    q = 1 # add by default
    if u < 0:
        q = 0
        u = -u

    args = dict( a=ra, b=rb, u=u, f=f, p=p, q=q, r=byte, t=t )
    if load:
        inst = arch.match( 0x04000000 )
    else:
        inst = arch.match( 0x04100000 )
    emit( inst.encode(args, getpc()) )

def str(ra, rb, u=0, pre=0, post=0, cc=''):
    return ldsr( 1, 0, ra, rb, u=u, pre=pre, post=post, cc=cc )

def strb(ra, rb, u=0, pre=0, post=0, cc=''):
    return ldsr( 1, 1, ra, rb, u=u, pre=pre, post=post, cc=cc )


def ldr(ra, rb, u=0, pre=0, post=0, cc=''):
    return ldsr( 0, 0, ra, rb, u=u, pre=pre, post=post, cc=cc )

def ldrb(ra, rb, u=0, pre=0, post=0, cc=''):
    return ldsr( 0, 1, ra, rb, u=u, pre=pre, post=post, cc=cc )


# branch instructions

def b(o, cc=''):
    f = arch.table['f'].index(cc)
    args = dict( o=o, f=f )
    inst = arch.match( 0x0a000000 ) # b
    emit( inst.encode(args, getpc()) )

def bl(o, cc=''):
    f = arch.table['f'].index(cc)
    args = dict( o=o, f=f )
    inst = arch.match( 0x0b000000 ) # bl
    emit( inst.encode(args, getpc()) )

def bx(ra, cc=''):
    f = arch.table['f'].index(cc)
    args = dict( a=ra, f=f )
    inst = arch.match( 0x012eff10 ) # bx
    emit( inst.encode(args, getpc()) )


# pseudo-instructons

def lsl(ra, shift, s=0, cc=''):
    aluri( 'mov', ra, 0, ra, shift, 'LSL', 0, cc )

def lsr(ra, shift, s=0, cc=''):
    aluri( 'mov', ra, 0, ra, shift, 'LSR', 0, cc )

def asr(ra, shift, s=0, cc=''):
    aluri( 'mov', ra, 0, ra, shift, 'ASR', 0, cc )

def ror(ra, shift, s=0, cc=''):
    aluri( 'mov', ra, 0, ra, shift, 'ROR', 0, cc )


def halt():
    b(getpc())
