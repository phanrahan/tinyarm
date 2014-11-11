ops = ["and", "eor", "sub", "rsb", "add", "adc", "sbc", "rsc", "tst", "teq", "cmp", "cmn", "orr", "mov", "bic", "mvn"]

print
print "# data operations register shifted immediate"
print
for op in ops:
    if op in ['mov', 'mvn']:
        print 'def %s(ra, rb):' % op
        print '    alu("%s", ra, 0, rb)' % op
    elif op in ['cmp', 'cmn', 'tst', 'teq']:
        print 'def %s(ra, rb):' % op
        print '    alu("%s", ra, 0, rb, s=1)' % op
    else:
        print 'def %s(ra, rb, rc):' % (op if op != 'and' else 'and_')
        print '    alu("%s", ra, rb, rc)' % op
    print

print
print "# data operations immediate"
print
for op in ops:
    if op in ['mov', 'mvn']:
        print 'def %si(ra, imm):' % op
        print '    alui("%si", ra, 0, imm)' % op
    elif op in ['cmp', 'cmn', 'tst', 'teq']:
        print 'def %si(ra, imm):' % op
        print '    alui("%si", ra, 0, imm, s=1)' % op
    else:
        print 'def %si(ra, rb, imm):' % op
        print '    alui("%si", ra, rb, imm)' % op
    print

