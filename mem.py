mem = 0
MAX = 0

def init(n):
    global mem, MAX
    MAX = n
    mem = bytearray(MAX)


def write8(addr, byte):
    global mem, MAX
    assert addr >= 0 and addr < MAX
    mem[addr] = byte

def write16(addr, halfword):
    write8( addr, halfword & 0xff )
    write8( addr+1, (halfword >> 8) & 0xff )

def write32(addr, word):
    write8( addr, word & 0xff )
    write8( addr+1, (word >> 8) & 0xff )
    write8( addr+2, (word >> 16) & 0xff )
    write8( addr+3, (word >> 24) & 0xff )


def read8(addr):
    global mem, MAX
    assert addr >= 0 and addr < MAX
    return mem[addr]

def read16(addr):
    byte0 = read8( addr )
    byte1 = read8( addr+1 )
    return (byte1 << 8) | byte0

def read32(addr):
    byte0 = read8( addr )
    byte1 = read8( addr+1 )
    byte2 = read8( addr+2 )
    byte3 = read8( addr+3 )
    return (byte3 << 24) | (byte2 << 16) | (byte1 << 8) | byte0


def savehex(filename, N=16, B=1):

    file = open(filename, 'w')

    # find largest non-zero data in memory
    n = len(mem)
    for i in range(0, n, 4):
        if read32(n-4-i) != 0:
            break
    last = n-i

    for addr in range(0, last, N):
        line = "%08X:" % addr
        for i in range(0,N,B):
            line += " "
            for j in range(B):
                byteaddr = addr + i + j
                if byteaddr < last:
                    line += "%02x" % mem[addr + i + j]
        print >> file, line

    file.close()

def savebin(filename, N=16, B=1):
    file = open(filename, 'w')

    # find largest non-zero data in memory
    n = len(mem)
    for i in range(0, n, 4):
        if read32(n-4-i) != 0:
            break
    last = n-i

    file.write(mem[0:last])

    file.close()

def save(filename='a.out'):
    savebin(filename)

def read(filename):
    bin = open(filename).read() 
    for i in range(len(bin)):
       mem[i] = ord(bin[i])
