PYTHONPATH=..

TESTS = badimm.hex \
	mov.hex \
	lsl.hex lsr.hex asr.hex ror.hex \
	alui.hex alu.hex \
    addi.hex add.hex add64.hex \
    sub.hex sub64.hex \
    z.hex n.hex \
    c1.hex c2.hex \
    v.hex \
    str.hex strb.hex strpre.hex strpost.hex \
	ldr.hex ldrb.hex \
    halt.hex \
    bne.hex

.PHONY: test gold clean

test: $(TESTS)

gold:
	for f in $(TESTS); do \
		cp $$f gold/$$f; \
	done

clean: 
	rm -f *.pyc *.hex *.bin

%.bin: %.py
	python $< 
	mv a.out $@

%.hex: %.bin
	hexdump -e '"%08_ax:"' -e '16/1 " %02x" "\n"' $*.bin > $*.hex
	if [ -e gold/$@ ] ; then \
		diff $@ gold/$@ ; \
	fi
