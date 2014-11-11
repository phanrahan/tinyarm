.PHONY: test gold clean

test: 
	make -C tests test

gold: 
	make -C tests gold

clean: 
	make -C tests clean
