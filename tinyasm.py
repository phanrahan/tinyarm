from mem import init, save, write8, write32

pc_ = 0
labels_ = {}

def assemble(prog, n):

    init(n)

    global pc_

    pc_ = 0
    prog()

    pc_ = 0
    prog()

def getpc():
    global pc_
    return pc_

def emit1(b):
    global pc_
    write8(pc_, b)
    pc_ += 1

def emit(w):
    global pc_
    write32(pc_, w)
    pc_ += 4

def org(addr):
    global pc_
    pc_ = addr


def equ(name, value):
    global labels_
    labels_[name] = value


def label(name=None):
    global labels_
    if not name:
        name = str(pc_)
    return labels_[name] if name in labels_ else pc_


def word(value):
    emit(value)


