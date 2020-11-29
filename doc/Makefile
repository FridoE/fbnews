INFODIR ?= /usr/share/info 
PREFIX ?= /usr/local/

all: info html

info: fbnews.info.gz
html: fbnews.html

fbnews.info.gz: fbnews.texi
	@makeinfo fbnews.texi
	@gzip -f fbnews.info

fbnews.html: fbnews.texi
	@LC_ALL=C makeinfo --html --no-split fbnews.texi

install: all	
	@cp fbnews.info.gz $(INFODIR)/fbnews.gz
	@cp fbnews.html $(PREFIX)/share/fbnews/

bogus:

clean: bogus
	@rm -f *~
	@rm -f fbnews.html
	@rm -f fbnews.info.gz
