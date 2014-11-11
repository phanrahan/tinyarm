ops = ["and", "eor", "sub", "rsb", "add", "adc", "sbc", "rsc", "tst", "teq", "cmp", "cmn", "orr", "mov", "bic", "mvn"]

# register shifted immediate
oprr = 'ffff 000%ss bbbb aaaa uuuu uhh0 cccc "%s%%(f)s%%(s)s r%%(a)d, r%%(b)d, r%%(c)d %%(h)s #%%(u)d"'

# register shifted register
opri = 'ffff 000%ss bbbb aaaa dddd 0hh1 cccc "%s%%(f)s%%(s)s r%%(a)d, r%%(b)d, r%%(c)d %%(h)s %%r(d)d"'

# immediate shifted
opi = 'ffff 001%ss bbbb aaaa iiii uuuu uuuu "%si%%(f)s%%(s)s r%%(a)d, r%%(b)d, #%%(u)d ROR %%(i)d"'

def opcode(i):
    s  = '1' if i & 8 else '0'
    s += ' '
    s += '1' if i & 4 else '0'
    s += '1' if i & 2 else '0'
    s += '1' if i & 1 else '0'
    return s

print "# data operations register shifted register"
for i in range(len(ops)):
    print oprr % (opcode(i), ops[i])

print
print "# data operations register shifted immediate"
for i in range(len(ops)):
    print opri % (opcode(i), ops[i])

print
print "# data operations shifted immediate"
for i in range(len(ops)):
    print opi % (opcode(i), ops[i])
