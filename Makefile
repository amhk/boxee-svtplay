boxee-bin := /opt/boxee/run-boxee-desktop

all: debug

debug: client
	$(boxee-bin)

.PHONY: client
client:
	$(MAKE) -C client

.PHONY: repository
repository: client
	$(MAKE) -C repository

clean:
	$(RM) -r out
