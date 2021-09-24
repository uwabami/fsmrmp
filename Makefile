SRCD = sourceFonts
DIST = dists
TMPD = tmp
VERSION = $(shell date '+%Y%m%d%H%M%S')
all: build

build: download
	@[ -d $(TMPD) ] || mkdir -p $(TMPD)
	@[ -d $(DIST) ] || mkdir -p $(DIST)
	@PYTHONPATH=$(CURDIR)/scripts \
	  python3 -c "import sys;import build; sys.exit(build.build('$(VERSION)'))"

download: dl_rmgen dl_twemoji dl_icons dl_agave

dl_agave:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/Agave-Regular.ttf ] ; then\
	  echo "Download Agave" ;\
	  wget https://github.com/blobject/agave/releases/latest/download/Agave-Regular.ttf \
	    -O $(SRCD)/Agave-Regular.ttf ;\
	  wget https://github.com/blobject/agave/releases/latest/download/Agave-Bold.ttf \
	    -O $(SRCD)/Agave-Bold.ttf ;\
	fi

dl_rmgen:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/rounded-x-mgenplus-1mn-regular.ttf ] ; then\
	  echo "Download Rounded Mgen+" ;\
	  wget https://osdn.jp/downloads/users/8/8599/rounded-x-mgenplus-20150602.7z ;\
	  unar rounded-x-mgenplus-20150602.7z ;\
	  cp -v rounded-x-mgenplus-20150602/rounded-x-mgenplus-1mn*.ttf $(SRCD)/ ;\
	  rm -fr rounded-x-mgenplus-20150602 ;\
	  rm -f rounded-x-mgenplus-20150602.7z ;\
	fi

dl_fsm:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/FantasqueSansMono-Regular.ttf ] ; then\
	  echo "Download Fantasque Sans Mono" ;\
	  wget https://fontlibrary.org/assets/downloads/fantasque-sans-mono/b0cbb25e73a9f8354e96d89524f613e7/fantasque-sans-mono.zip ;\
	  unar fantasque-sans-mono.zip ;\
	  cp -v fantasque-sans-mono/*.ttf $(SRCD)/ ;\
	  rm -fr fantasque-sans-mono ;\
	  rm -f fantasque-sans-mono.zip ;\
	fi

dl_twemoji:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/TwitterColorEmoji-SVGinOT-ThickFallback.ttf ] ; then\
	  echo "Download Twitter Color Emoji SVG in OpenType" ;\
	  wget https://github.com/eosrei/twemoji-color-font/releases/download/v13.0.1/TwitterColorEmoji-SVGinOT-ThickFallback-13.0.1.zip ;\
	  unar TwitterColorEmoji-SVGinOT-ThickFallback-13.0.1.zip ;\
	  cp -v TwitterColorEmoji-SVGinOT-ThickFallback-13.0.1/*.ttf $(SRCD)/ ;\
	  rm -fr TwitterColorEmoji-SVGinOT-ThickFallback-13.0.1 ;\
	  rm -f TwitterColorEmoji-SVGinOT-ThickFallback-13.0.1.zip ;\
	fi

dl_symbola:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/Symbola.otf ] ; then\
	  echo "Download Symbola: Multilingual support and Symbol blocks of The Unicode Standard" ;\
	  wget https://dn-works.com/wp-content/uploads/2020/UFAS-Fonts/Symbola.zip ;\
	  unar Symbola.zip ;\
	  cp -v Symbola/Symbola.otf $(SRCD)/ ;\
	  rm -fr Symbola ;\
	  rm -f Symbola.zip ;\
	fi

dl_icons:
	@if [ ! -f $(SRCD)/isfit-plus.ttf ] ; then\
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
