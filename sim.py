import os
import sys

import mem
from arch import Arch
from bits import lsl, lsr, asr, ror

__all__  = ['read32', 'write32']
__all__ += ['readreg', 'writereg']
__all__ += ['readcpsr', 'CPSR_Z', 'CPSR_N', 'CPSR_C', 'CPSR_V']
__all__ += ['load', 'reset', 'execute', 'arch']

arch = Arch('arm.arch')

TRACE = 0

SIGN = 0x80000000
DATAMASK = 0xffffffff

ADDRMASK = 0x1fffff
MAXADDR	= ADDRMASK+1

mem.init(MAXADDR)

CPSR_N	= (1<<31)
CPSR_Z	= (1<<30)
CPSR_C	= (1<<29)
CPSR_V	= (1<<28)
cpsr = 0

reg = 16*[0]
pc = 0

def read32( addr ):
    if addr & 0x3:
        raise "Unaligned memory access"

    if addr >= 0x2000000:
        print 'reading from peripheral register', '%08x' % addr
        return 0

    else:
        if addr < 0 or addr >= MAXADDR:
            #raise 'Memory Fault'
            print "Memory Fault"
            sys.exit(0)
        else:
            return mem.read32(addr)

def write32( addr, word ):
    if addr & 0x3:
        raise "Unaligned memory access"

    if addr >= 0x2000000:
        print 'peripheral register %08x = %08x' % (addr, word)

    else:
        if addr < 0 or addr >= MAXADDR:
            #raise 'Memory Fault'
            print "Memory Fault"
            sys.exit(0)
        else:
            mem.write32(addr, word)
            print 'mem[%08x] = %08x' % (addr, word)


def readreg( r ):
    global reg
    assert r >= 0 and r < 16
    data=reg[r]
    return data

def writereg( r, data ):
    global reg
    assert r >= 0 and r < 16
    if TRACE or r != 15:
        if r == 15:
            print 'pc = %08x' % data
        elif r == 14:
            print 'lr = %08x' % data
        elif r == 13:
            print 'sp = %08x' % data
        else:
            print 'r%d = %08x' % (r, data)
    reg[r]=data

def printcc():
    print 'Z=%d' % (1 if cpsr & CPSR_Z else 0),
    print 'N=%d' % (1 if cpsr & CPSR_N else 0),
    print 'C=%d' % (1 if cpsr & CPSR_C else 0),
    print 'V=%d' % (1 if cpsr & CPSR_V else 0),
    print

def logic( res, s ):
    if s:
        global cpsr

        if res==0: cpsr |=  CPSR_Z
        else:      cpsr &= ~CPSR_Z

        if res&SIGN: cpsr |=  CPSR_N
        else:        cpsr &= ~CPSR_N

        #printcc()

    return res

def adder( a, b, c, s ):
    res = a + b + c;
    carry = res & (DATAMASK+1);
    res &= DATAMASK

    if s:
        global cpsr

        if carry: cpsr |=  CPSR_C
        else:     cpsr &= ~CPSR_C

        v = (a^res) & (b^res) & SIGN
        if v: cpsr |=  CPSR_V
        else: cpsr &= ~CPSR_V

        logic(res, s)

    return res


def readcpsr():
    return cpsr

def carry():
    return 1 if cpsr & CPSR_C else 0

def borrow():
    return 0 if cpsr & CPSR_C else 1


def pred( op ):
    op = arch.table['f'].index(op)

    if op == 0: return cpsr&CPSR_Z #Q
    if op == 1: return not (cpsr&CPSR_Z)
    if op == 2: return cpsr&CPSR_C
    if op == 3: return not (cpsr&CPSR_C)
    if op == 4: return cpsr&CPSR_N
    if op == 5: return not (cpsr&CPSR_N)
    if op == 6: return cpsr&CPSR_V
    if op == 7: return not (cpsr&CPSR_V)

    if op == 8: return (cpsr&CPSR_C) and (not (cpsr&CPSR_Z))
    if op == 9: return (cpsr&CPSR_Z) or (not (cpsr&CPSR_C))

    if op == 0xa: 
        ra=False
        if (cpsr&CPSR_N) and (cpsr&CPSR_V): ra = True
        if (not (cpsr&CPSR_N)) and (not (cpsr&CPSR_V)): ra = True
        return ra

    if op == 0xb: 
        ra=False
        if (not (cpsr&CPSR_N)) and (cpsr&CPSR_V): ra = True
        if (not (cpsr&CPSR_V)) and (cpsr&CPSR_N): ra = True
        return ra

    if op == 0xc: 
        ra=False
        if   (cpsr&CPSR_N) and (cpsr&CPSR_V) : ra = True
        if (not (cpsr&CPSR_N)) and (not (cpsr&CPSR_V)): True
        if cpsr&CPSR_Z: ra=FALSE
        return ra

    if op == 0xd: 
        ra=False
        if (not (cpsr&CPSR_N)) and (cpsr&CPSR_V): ra = True
        if (not (cpsr&CPSR_V)) and (cpsr&CPSR_N): ra = True
        if cpsr&CPSR_Z: ra = True
        return ra

    return True

def invert(i):
    return (~i) & DATAMASK

def rotate(i, r):
    res =  (i >> r) | ((i << (32-r)) & 0xffffffff)
    return res

def barrelshift(i, shift, shifttype):
    if   shifttype == 'LSL':
        res = lsl(i, shift)
    elif shifttype == 'LSR':
        res = lsr(i, shift)
    elif shifttype == 'ASR':
        res = asr(i, shift)
    elif shifttype == 'ROR':
        res = ror(i, shift)
    return res

def fetch():
    machinecode=read32(pc)
    return pc, machinecode

def decode(code, addr):
    return arch.decode( code, addr )

def execute ():
    addr, code  = fetch()
    inst = decode(code, addr+8)

    #print "%08x" % addr, "%08x:" % code, inst.dis()

    nextpc = addr + 4

    cc = inst.f
    if pred( cc ):
        # alu
        if inst.type == 0x0:
            if code & 0x012eff10 == 0x012eff10:
                ra = inst.a
                nextpc = readreg(ra)

            elif (code & 0x0e000000) == 0x00000000:
                if (code & 0x0e000090) == 0x00000010:
                    raise 'Unimplemented Instruction'

            else:

                s = inst.s
                ra = inst.a
                rb = inst.b

                b = readreg(rb)

                if code & 0x02000000: # immediate flag
                    c = rotate(inst.u, 2*inst.i)
                else:
                    rc = inst.c
                    c = readreg(rc)
                    # register shift register
                    if code & 0x00000010:
                        shift = readreg(inst.d)
                    # register shift immediate
                    else:
                        shift = inst.u
                    c = barrelshift( c, shift, inst.h )

                if   inst.q == 'and': 
                    writereg(ra, logic( b & c, s ) )

                elif inst.q == 'eor':
                    writereg(ra, logic( b ^ c, s ) )

                elif inst.q == 'sub': 
                    writereg(ra, adder( b, invert(c), 1, s ) )

                elif inst.q == 'rsb': 
                    writereg(ra, adder( invert(b), c, 1, s ) )

                elif inst.q == 'add':
                    writereg(ra, adder( b, c, 0, s ) )

                elif inst.q == 'adc':
                    # b + c + carry
                    writereg(ra, adder( b, c, carry(), s ) )

                elif inst.q == 'sbc': 
                    # b - c - 1 + carry
                    writereg(ra, adder( b, invert(c), carry(), s ) )

                elif inst.q == 'rsc':
                    # c - b - 1 + carry
                    writereg(ra, adder( invert(b), c, carry(), s ) )

                elif inst.q == 'tst':
                    a = readreg(ra)
                    logic( a & c, s)

                elif inst.q == 'teq': 
                    a = readreg(ra)
                    logic( a ^ c, s)

                elif inst.q == 'cmp':
                    a = readreg(ra)
                    adder( a, invert(c), 1, s )

                elif inst.q == 'cmn':
                    a = readreg(ra)
                    adder( a, c, 0, s )

                elif inst.q == 'orr':
                    writereg(ra, logic( b | c, s ) )

                elif inst.q == 'mov':
                    writereg(ra, logic( c, s ) )

                elif inst.q == 'bic':
                    writereg(ra, logic( b & invert(c), s ) )

                elif inst.q == 'mvn':
                    writereg(ra, logic( invert(c), s ) )

                else:
                    raise "Uniplemented Instruction"

        # LDR/STR
        elif inst.type == 0x1:
            ra = inst.a
            rb = inst.b

            b = readreg(rb)

            # immediate
            i = 1 if code & 0x02000000 else 0
            if i:
                # immediate
                u = readreg(inst.c) << inst.u
            else: 
                # shifted register
                u = inst.u

            # down=0 up=1 - different mnenomic
            bindex = b+u if inst.q else b-u

            # pre-index
            if inst.p == 1: 
                b = bindex

            if code & 0x00100000: # LDR
                # word=0 byte=1
                if inst.r: # b
                    raise 'LDRB not implemented'
                else:
                    a = read32(b)
                    writereg(ra,a)
            else: # STR
                if inst.r: # b
                    raise 'STRB not implemented'
                else:
                    a = readreg(ra)
                    write32(b,a)

            # post-index
            if inst.p == 0: 
                b = bindex

            # write-back
            if inst.t: # w different mnenomic
                writereg(rb, b)

        elif inst.type == 0x2:
            if code == 0xeafffffe: # halt
                print 'halt'
                return 1

            if (code & 0x0e000000) == 0x0a000000:

                o = inst.o
                # the pc must be adjusted to point immediately following the bl
                if code & 0x01000000: # bl
                    writereg(14,reg[15]-4)
                nextpc = o

            # block data transfer
            else:
                 raise "Uniplemented Instruction"

        else:
             raise "Uniplemented Instruction"

    global pc
    pc = nextpc
    writereg(15, nextpc+8)

    return 0


def reset():
    global reg, cpsr, pc
    for i in range(15):
        reg[0] = 0

    pc = 0
    reg[15] = pc + 0x08

    cpsr = 0

def load(filename):
    mem.read(filename)
    reset()

