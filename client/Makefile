appname := net.kongstadbrun.svtplay
out := ../out/$(appname)
xmls := $(out)/descriptor.xml $(out)/skin/Boxee\ Skin\ NG/720p/main.xml

SHELL := bash

$(out)/%.xml: %.xml sub.awk
	@echo "[APP] $<"
	@mkdir -p $(out)
	@awk -f sub.awk "$<" | tidy -xml -utf8 -qi -w 80 -o "$@" && \
		test $${PIPESTATUS[0]} -eq 0 || (rm -f "$@" && false)


$(out)/skin/Boxee\ Skin\ NG/720p/%.xml: %.xml sub.awk
	@echo "[APP] $<"
	@mkdir -p $(out)/skin/Boxee\ Skin\ NG/720p
	@awk -f sub.awk "$<" | tidy -xml -utf8 -qi -w 80 -o "$@" && \
		test $${PIPESTATUS[0]} -eq 0 || (rm -f "$@" && false)

all: $(xmls)

clean:
	rm -rf $(out)
