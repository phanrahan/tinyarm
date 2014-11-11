
from asm import *

def prog():
    halt()

assemble(prog, 0x100)

save()

