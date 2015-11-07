PYTHON=python3
LOGLEVEL=--log-level=debug
LOGLEVEL=--log-level=info
#LOGLEVEL=--log-level=warning
#LOGLEVEL=--log-level=error

OPTIONS=$(LOGLEVEL)


all:
	$(PYTHON) -m neural_world $(OPTIONS)
