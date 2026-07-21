FONT=fonts/ttf/X11Fixed10x20-Regular.ttf
ORIGINAL=fonts/ttf/Fixed20-Original.ttf
SOURCE=fonts/original/iso/10x20.pcf.gz

.PHONY: all specimens check clean

all: $(FONT) specimens

$(FONT): $(SOURCE) tools/build_ttf.py
	python3 tools/build_ttf.py $(SOURCE) $(FONT)
	cp $(FONT) docs/assets/

specimens: $(ORIGINAL)
	python3 tools/make_specimens.py

check: $(FONT)
	python3 -m fontTools.ttLib.woff2 compress $(FONT) /tmp/X11Fixed10x20-Regular.woff2
	fc-scan $(FONT) >/dev/null

clean:
	$(RM) $(FONT) specimens/*.png docs/assets/X11Fixed10x20-Regular.ttf
