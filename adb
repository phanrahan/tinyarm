#!/usr/bin/env python
import os
import sys
import signal

from sim import *

halt = 0

def interupt(signal, frame):
    global halt
    if not halt:
        halt = 1
        print 'halt'

def step():
    execute()

def cont():
    global halt
    halt = 0
    while not halt:
        halt = execute()
    print 'halt'

def info():
    for r in range(16):
        reg = readreg(r)
        if   r == 15:
            print 'pc  = %08x' % reg
        elif r == 14:
            print 'lr  = %08x' % reg
        elif r == 13:
            print 'sp  = %08x' % reg
        else:
            print 'r%d  = %08x' % (r, reg)
    cpsr = readcpsr()
    print 'Z=%d' % (1 if cpsr & CPSR_Z else 0),
    print 'N=%d' % (1 if cpsr & CPSR_N else 0),
    print 'C=%d' % (1 if cpsr & CPSR_C else 0),
    print 'V=%d' % (1 if cpsr & CPSR_V else 0),
    print

def list():
    pc = readreg(15) - 8
    for addr in range(pc,pc+64,4):
        code = read32(addr)
        inst = arch.decode(code,addr+8)
        print "%08x" % addr, "%08x:" % code, inst.dis()


def adb ( ):
    while True:
        line = raw_input('arm> ')
        args = line.split()
        if len(args) > 0:
            arg0 = args[0] 
            if    arg0.startswith('r'):
                reset()
            elif  arg0.startswith('c'):
                cont()
            elif  arg0.startswith('s'):
                step()
            elif arg0.startswith('i'):
                info()
            elif arg0.startswith('l'):
                list()
            elif arg0.startswith('mr'):
                if len(args) == 2:
                    addr = eval(args[1])
                    data = read32(addr)
                    print "%08x" % addr, "%08x:" % data 
            elif arg0.startswith('mw'):
                if len(args) == 3:
                    addr = eval(args[1])
                    data = eval(args[2])
                    write32(addr, data)
                    print "%08x" % addr, "%08x:" % data 
            elif arg0.startswith('e') or arg0.startswith('q'):
                return
            else:
                pass

filename = 'a.out'
if len(sys.argv)>1:
    filename = sys.argv[1]

signal.signal(signal.SIGINT, interupt)

try:
    load( filename )
    adb()
except EOFError:
    pass

