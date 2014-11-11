import sys
from arch import Arch

arch = Arch('arm.arch')

for inst in arch.instructions:
    print "%08x" % inst.bits, inst.action

