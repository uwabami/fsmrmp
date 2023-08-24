SRCD = sourceFonts
DIST = dists
TMPD = tmp
NERD = FontPatcher
VERSION = $(shell date '+%Y%m%d%H%M%S')
all: build

build: download
	@[ -d $(TMPD) ] || mkdir -p $(TMPD)
	@[ -d $(DIST) ] || mkdir -p $(DIST)
	@PYTHONPATH=$(CURDIR)/scripts \
	  python3 -c "import sys;import build; sys.exit(build.build('$(VERSION)'))"

download: dl_rmgen dl_fsm dl_notoemoji dl_isfit

dl_rmgen:
	@[ -d $(SRCD) ] ||	mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/rounded-x-mgenplus-1mn-regular.ttf ] ; then\
	  echo "Download Rounded Mgen+" ;\
	  wget https://ftp.iij.ad.jp/pub/osdn.jp/users/8/8599/rounded-x-mgenplus-20150602.7z ;\
	  unar rounded-x-mgenplus-20150602.7z ;\
	  cp -v rounded-x-mgenplus-20150602/rounded-x-mgenplus-1mn*.ttf $(SRCD)/ ;\
	  rm -fr rounded-x-mgenplus-20150602 ;\
	  rm -f rounded-x-mgenplus-20150602.7z ;\
	fi

dl_fsm:
	@[ -d $(SRCD) ] ||	mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/FantasqueSansMono-Regular.ttf ] ; then\
	  echo "Download Fantasque Sans Mono" ;\
	  wget https://fontlibrary.org/assets/downloads/fantasque-sans-mono/b0cbb25e73a9f8354e96d89524f613e7/fantasque-sans-mono.zip ;\
	  unar fantasque-sans-mono.zip ;\
	  cp -v fantasque-sans-mono/*.ttf $(SRCD)/ ;\
	  rm -fr fantasque-sans-mono ;\
	  rm -f fantasque-sans-mono.zip ;\
	fi

dl_notoemoji:
	@[ -d $(SRCD) ] ||	mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/NotoEmoji-Regular.ttf ] ; then\
	  echo "Download Noto Emoji Monchrome" ;\
	  wget "https://fonts.google.com/download?family=Noto%20Emoji" -O Emoji.zip;\
	  unar Emoji.zip ;\
	  cp -v Emoji/static/NotoEmoji-Regular.ttf $(SRCD)/ ;\
	  rm -fr Emoji ;\
	  rm -f Emoji.zip ;\
	fi

dl_isfit:
	@[ -d $(SRCD) ] ||	mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/isfit-plus.ttf ] ; then\
	  echo "Download isfit+" ;\
	  wget https://github.com/uwabami/isfit-plus/raw/master/dists/isfit-plus.ttf -O $(SRCD)/isfit-plus.ttf ;\
	fi

clean:
	@rm -f scripts/*.pyc

distclean: clean
	rm -fr $(SRCD)/*.ttf
	rm -fr $(SRCD)/*.otf
	rm -fr $(DIST)/*.ttf
	rm -fr $(TMPD)
	rm -fr $(SRCD)
	rm -fr $(DIST)
