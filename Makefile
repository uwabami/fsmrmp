SRCD = sourceFonts
DIST = dists
TMPD = tmp
VERSION = $(shell date '+%Y%m%d%H%M%S')
all: build

build: download
	@[ -d $(TMPD) ] || mkdir -p $(TMPD)
	PYTHONPATH=$(CURDIR)/scripts \
	  python2 -c "import sys;import build; sys.exit(build.build('$(VERSION)'))"

download: download_rmgen download_fsm download_symbola

download_rmgen:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/rounded-x-mgenplus-1mn-regular.ttf ] ; then\
	  echo "Download Rounded Mgen+" ;\
	  wget https://osdn.jp/downloads/users/8/8599/rounded-x-mgenplus-20150602.7z ;\
	  unar rounded-x-mgenplus-20150602.7z ;\
	  cp -v rounded-x-mgenplus-20150602/rounded-x-mgenplus-1mn*.ttf $(SRCD)/ ;\
	  rm -fr rounded-x-mgenplus-20150602 ;\
	  rm -f rounded-x-mgenplus-20150602.7z ;\
	fi

download_fsm:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/FantasqueSansMono-Regular.ttf ] ; then\
	  echo "Download Fantasque Sans Mono" ;\
	  wget https://fontlibrary.org/assets/downloads/fantasque-sans-mono/b0cbb25e73a9f8354e96d89524f613e7/fantasque-sans-mono.zip ;\
	  unar fantasque-sans-mono.zip ;\
	  cp -v fantasque-sans-mono/*.ttf $(SRCD)/ ;\
	  rm -fr fantasque-sans-mono ;\
	  rm -f fantasque-sans-mono.zip ;\
	fi

download_symbola:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/Symbola_Hinted.ttf ] ; then\
	  echo "Download Symbola" ;\
	  wget http://users.teilar.gr/~g1951d/Symbola.zip ;\
	  unar Symbola.zip ;\
	  cp -v Symbola/*.ttf $(SRCD)/ ;\
	  rm -fr Symbola ;\
	  rm -f Symbola.zip ;\
	fi

clean:
	@rm -f  fantasque-sans-mono.zip
	@rm -fr fantasque-sans-mono
	@rm -fr rounded-x-mgenplus-20150602
	@rm -f  rounded-x-mgenplus-20150602.7z
	@rm -fr Symbola
	@rm -f  Symbola.zip

distclean: clean
	rm -fr $(SRCD)
	rm -fr $(DIST)
	rm -fr $(TMPD)
