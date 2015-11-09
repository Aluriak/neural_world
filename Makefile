PYTHON=python3
LOGLEVEL=--log-level=debug
LOGLEVEL=--log-level=info
#LOGLEVEL=--log-level=warning
#LOGLEVEL=--log-level=error
#NOGRAPH=--render-png=0

OPTIONS=$(LOGLEVEL) $(NOGRAPH)


all:
	$(PYTHON) -m neural_world $(OPTIONS)
