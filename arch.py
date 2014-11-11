import sys
from bits import *

class DecodedInst:
    def __init__(self, inst, code, addr, args):
        self.inst = inst
        self.code = code
        self.addr = addr
        self.args = args
        for c in args:
            setattr(self,c,args[c])
        setattr(self, 'type', (code >> 26) & 0x3 )

    def dis(self):
        args = {}
        for k, v in self.args.items():
            if k == 's':
                v = 's' if v else ''
            args[k] = v
        return self.inst.action % args
    

class Inst:
    def __init__(self, arch, pattern, action):
        self.arch = arch
        self.pattern = pattern
        self.action = action
        self.parse()

        #print pattern, action, "%08x" % self.bits, "%08x" % self.mask, self.fields

    def __str__(self):
        return self.action

    def parse(self):
        self.mask = 0
        self.bits = 0
        self.fields = {}
        for i in range(len(self.pattern)):
            c = self.pattern[i]
            if c != ' ' and c != '\t':
                self.bits <<= 1
                self.mask <<= 1
                if c == '0' or c == '1':
                    self.bits |= (c == '1')
                    self.mask |= (c == '0' or c == '1')
                else:
                    if c not in  self.fields:
                        s = c in self.arch.signed
                        self.fields[c] = dict( i=self.arch.word-i, n=1, signed=s )
                    else:
                        self.fields[c]['n'] += 1

    def match(self, code):
        return (self.mask & code) == self.bits

    def encode(self, args, addr):
        inst = self.bits
        for key in self.fields.keys():
            field = self.fields[key]
            i = field['i']
            n = field['n']
            val = args.get(key, 0)
            if key == 'o':
               val = (val-addr-8)/4

            if field['signed']:
                val = checks( val, n )
            else:       
                val = checku( val, n )

            val <<= i - n
            inst |= val 
        return inst

    def bind(self, code, addr):
        args = {}
        for i in range(len(self.pattern)):
            c = self.pattern[i]
            if c == ' ' or c == '\t' or c == '0' or c == '1':
                continue

            bit = 1 if (code & (1 << (self.arch.word-1-i))) else 0
            if c not in args:
                args[c] = 0
            args[c] = (args[c] << 1) | bit

        for c in args:
            if c in self.arch.signed and self.arch.signed[c]:
                if args[c] & (1 << 23):
                    args[c] &= ~(1 << 23)
                    args[c] -=  (1 << 23)

            if c in self.arch.table:
                args[c] = self.arch.table[c][args[c]]
            if c == 'o':
                args[c] = addr + 4*args[c]

        return args

    def decode(self, code, addr):
        args = self.bind(code, addr)
        return DecodedInst( self, code, addr, args )


class Arch:

    def __init__(self, filename):
        self.instructions = []

        self.signed = {}
        self.offset = {}
        self.table = {}

        self.word = 32
        self.littleendian = True

        self.parse(filename)

    def parseinst(self, line):
        pattern = ''
        action = ''
        for i in range(len(line)):
            c = line[i]
            if c == ' ' or c == '\t':
                continue
            elif c == '#' or c == '\n' or c == '\r':
                break
            elif (c >= 'a' and c <= 'z') or c == '0' or c == '1':
                pattern = pattern + c
            elif c == '"':
                rest = line[i + 1:]
                n = rest.find('"')
                action = rest[:n]
                return Inst(self, pattern, action)

    def parse(self, filename):
        lines = open(filename).readlines()

        for line in lines:

            if line.startswith('word'):
                self.word = int(line.split()[1])
                #print 'word', word
            elif line.startswith('little-endian'):
                self.littleendian = True
            elif line.startswith('big-endian'):
                self.littleendian = False
            elif line.startswith('signed'):
                self.signed[line[7]] = True
                #print 'signed', line[7], self.signed[line[7]]
            elif line.startswith('unsigned'):
                self.signed[line[7]] = False
                #print 'unsigned', line[7], self.signed[line[7]]
            elif line.startswith('offset'):
                self.signed[line[7]] = True
                self.offset[line[7]] = True
            elif line.startswith('table'):
                self.table[line[6]] = eval(line[7:])
                #print 'table', line[6], self.table[line[6]]
            else:
                inst = self.parseinst(line)
                if inst:
                    self.instructions.append( inst )

    def match(self, code):
        for inst in self.instructions:
           if inst.match(code):
               return inst

    def decode(self, code, addr):
        inst = self.match(code)
        return inst.decode(code, addr)

    def dis(self, code, addr):
        inst = self.decode(code, addr)
        return inst.dis()
