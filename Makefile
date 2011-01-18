boxee-bin := /opt/boxee/run-boxee-desktop

all: debug

debug:
	$(MAKE) -C client debug
	$(boxee-bin)

.PHONY: repository
repository:
	$(MAKE) -C client release
	$(MAKE) -C repository

clean:
	$(RM) -r out
	$(MAKE) -C server clean
