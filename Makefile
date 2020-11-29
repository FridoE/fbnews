INSTALLPREFIX = /usr/local
INSTALLFILES = $(wildcard *.py) TODO README COPYING fbnewsrc startmoz.sh
PACKAGE = fbnews-0.5

all: 
	@make -C doc

dist:
	@tla inventory -sB | tar -cf - --no-recursion -T- | (mkdir $(PACKAGE);cd $(PACKAGE);tar xf -)
	@tar czf $(PACKAGE).tar.gz $(PACKAGE)
	@rm $(PACKAGE) -rf
install:
	@mkdir -p $(INSTALLPREFIX)/share/fbnews
	@make PREFIX=$(INSTALLPREFIX) -C doc install
	@cp -f $(INSTALLFILES) $(INSTALLPREFIX)/share/fbnews/
	@chmod +x $(INSTALLPREFIX)/share/fbnews/fbnews.py
	@ln -sf $(INSTALLPREFIX)/share/fbnews/fbnews.py \
		$(INSTALLPREFIX)/bin/fbnews
	@ln -sf $(INSTALLPREFIX)/share/fbnews/startmoz.sh \
		$(INSTALLPREFIX)/bin/startmoz
	@echo "fbnews installed. "
	@echo "Please copy the file fbnewsrc into your ~/."\
		"fluxbox directory and adapt it to your needs."

uninstall:
	@rm -rf $(INSTALLPREFIX)/share/fbnews
	@rm -f $(INSTALLPREFIX)/bin/fbnews

clean:
	@rm -f *~
	@rm -f *.pyc
	@make -C doc clean
