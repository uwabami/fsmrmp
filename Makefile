SRCD = sourceFonts
DIST = dists
TMPD = tmp
VERSION = $(shell date '+%Y%m%d%H%M%S')
all: build

build: download
	@[ -d $(TMPD) ] || mkdir -p $(TMPD)
	@PYTHONPATH=$(CURDIR)/scripts \
	  python2 -c "import sys;import build; sys.exit(build.build('$(VERSION)'))"

download: dl_rmgen dl_fsm dl_twemoji
dl_symbols: dl_devicons dl_iec_symbols dl_powerline_extra_symbols dl_powerline_symbols dl_fontawesome dl_fontawesome_ext dl_materialdesign dl_octicons dl_logos dl_weather dl_nerd dl_fileicons dl_alltheicons

patch: dl_symbols
	@if [ ! -f $(TMPD)/FSMRMP-Regular.ttf ] ; then\
	  echo "run 'make build' before 'make patch'" ;\
	else \
	  PYTHONPATH=$(CURDIR)/scripts python2 -c "import sys;import font_patcher; sys.exit(font_patcher.build())" ;\
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
	@if [ ! -f $(SRCD)/TwitterColorEmoji-SVGinOT.ttf ] ; then\
	  echo "Download Twitter Color Emoji SVG in OpenType" ;\
	  wget https://github.com/eosrei/twemoji-color-font/releases/download/v12.0.1/TwitterColorEmoji-SVGinOT-12.0.1.zip ;\
	  unar TwitterColorEmoji-SVGinOT-12.0.1.zip ;\
	  cp -v TwitterColorEmoji-SVGinOT-12.0.1/*.ttf $(SRCD)/ ;\
	  rm -fr TwitterColorEmoji-SVGinOT-12.0.1 ;\
	  rm -f TwitterColorEmoji-SVGinOT-12.0.1.zip ;\
	fi

dl_symbola:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/Symbola_Hinted.ttf ] ; then\
	  echo "Download Symbola" ;\
	  wget http://users.teilar.gr/~g1951d/Symbola.zip ;\
	  unar Symbola.zip ;\
	  cp -v Symbola/*.ttf $(SRCD)/ ;\
	  rm -fr Symbola ;\
	  rm -f Symbola.zip ;\
	fi

dl_devicons:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/devicons.ttf ] ; then\
	  wget https://github.com/vorillaz/devicons/raw/master/fonts/devicons.ttf -O $(SRCD)/devicons.ttf ;\
	fi

dl_iec_symbols:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/Unicode_IEC_symbol_font.otf ] ; then\
	  wget https://github.com/jloughry/Unicode/raw/4c79c6a81f29584e18f827b07c0bf6f02fc3ebbe/Unicode_IEC_symbol_font.otf -O $(SRCD)/Unicode_IEC_symbol_font.otf ;\
	fi

dl_powerline_extra_symbols:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/PowerlineExtraSymbols.otf ] ; then\
	  echo "Download Powerline Extra Symbols" ;\
	  wget https://github.com/ryanoasis/powerline-extra-symbols/raw/90b84948574773f8a2f08bcd26718f7c158f7a41/PowerlineExtraSymbols.otf -O $(SRCD)/PowerlineExtraSymbols.otf ;\
	fi

dl_powerline_symbols:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/PowerlineSymbols.otf ] ; then\
	  echo "Download Powerline Symbols" ;\
	  wget https://github.com/powerline/powerline/raw/c1bf60dbcea9029be7e1eb492b570aaa248acf41/font/PowerlineSymbols.otf -O $(SRCD)/PowerlineSymbols.otf ;\
	fi

dl_fontawesome:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/FontAwesome.otf ] ; then\
	  echo "Download FontAwesome v4.7.0" ;\
	  wget https://github.com/FortAwesome/Font-Awesome/archive/v4.7.0.zip ;\
	  unar v4.7.0.zip ;\
	  cp -v Font-Awesome-4.7.0/fonts/FontAwesome.otf sourceFonts ;\
	  rm -fr Font-Awesome-4.7.0 ;\
	  rm -f v4.7.0.zip ;\
	fi

dl_fontawesome_ext:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/font-awesome-extension.ttf ] ; then\
	  wget https://github.com/AndreLZGava/font-awesome-extension/raw/master/fonts/font-awesome-extension.ttf -O $(SRCD)/font-awesome-extension.ttf ;\
	fi

dl_materialdesign:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/materialdesignicons-webfont.ttf ] ; then\
	  echo "Download MaterialDesignIcons " ;\
	  wget https://github.com/Templarian/MaterialDesign-Webfont/raw/v3.6.95/fonts/materialdesignicons-webfont.ttf -O $(SRCD)/materialdesignicons-webfont.ttf ;\
	fi

dl_octicons:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/octicons.ttf ] ; then\
	  echo "Download Octicons " ;\
	  wget https://github.com/primer/octicons/archive/v4.4.0.zip ;\
	  unar v4.4.0.zip ;\
	  cp -v octicons-4.4.0/build/font/octicons.ttf $(SRCD)/octicons.ttf ;\
	  rm -fr octicons-4.4.0 ;\
	  rm -f v4.4.0.zip ;\
	fi

dl_logos:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/font-logos.ttf ] ; then\
	  wget https://github.com/lukas-w/font-logos/raw/v0.11/assets/font-logos.ttf -O $(SRCD)/font-logos.ttf ;\
	fi

dl_weather:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/weathericons-regular-webfont.ttf ] ; then\
	  wget https://github.com/erikflowers/weather-icons/raw/2.0.10/font/weathericons-regular-webfont.ttf -O $(SRCD)/weathericons-regular-webfont.ttf ;\
	fi

dl_nerd:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/nerd-original-sources.otf ] ; then\
	  wget https://github.com/ryanoasis/nerd-fonts/raw/a516f740938f9eff28de9b7c981c210005d86e38/src/glyphs/original-source.otf -O $(SRCD)/nerd-original-sources.otf ;\
	fi

dl_fileicons:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/file-icons.ttf ] ; then\
	  wget https://github.com/file-icons/icons/raw/de534d36a6e18c8d4a4c61eb41f3e5bfb7eccda8/dist/file-icons.woff2 ;\
	  woff2_decompress file-icons.woff2 ;\
	  mv file-icons.ttf $(SRCD)/ ;\
	  rm -f file-icons.woff2 ;\
	fi

dl_alltheicons:
	@[ -d $(SRCD) ] ||  mkdir -p $(SRCD)
	@if [ ! -f $(SRCD)/all-the-icons.ttf ] ; then\
	  wget https://github.com/domtronn/all-the-icons.el/raw/52d1f2d36468146c93aaf11399f581401a233306/fonts/all-the-icons.ttf -O $(SRCD)/all-the-icons.ttf ;\
	fi

clean:
	@rm -f scripts/*.pyc
	@rm -f  fantasque-sans-mono.zip
	@rm -fr fantasque-sans-mono
	@rm -fr rounded-x-mgenplus-20150602
	@rm -f  rounded-x-mgenplus-20150602.7z
	@rm -fr Symbola
	@rm -f  Symbola.zip

distclean: clean
	rm -fr $(SRCD)/*.ttf
	rm -fr $(SRCD)/*.otf
	rm -fr $(DIST)/*.ttf
	rm -fr $(TMPD)
