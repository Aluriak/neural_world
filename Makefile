PYTHON=python3
LOGLEVEL=--log-level=debug
LOGLEVEL=--log-level=info
#LOGLEVEL=--log-level=warning
#LOGLEVEL=--log-level=error
#NOGRAPH=--render-png=0

OPTIONS=$(LOGLEVEL) $(NOGRAPH)


sim:
	$(PYTHON) -m neural_world simulation $(OPTIONS)

indiv:
	$(PYTHON) -m neural_world individual $(OPTIONS)

test:
	$(PYTHON) -m unittest discover -v
