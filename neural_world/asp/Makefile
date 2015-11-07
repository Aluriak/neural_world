GRINGO=/usr/lib/python3.5/site-packages/pyasp/bin/gringo4
CLASP=/usr/lib/python3.5/site-packages/pyasp/bin/clasp
CLASP_OPTIONS=-n 0
GROUNDED_DATA=grounded_data


neural_solving: neural_solving_ solve
neural_solving_:
	$(GRINGO) neural_solving.lp neural_solving_datatest.lp > $(GROUNDED_DATA)

solve:
	$(CLASP) $(CLASP_OPTIONS) < $(GROUNDED_DATA)


v:
	$(GRINGO) -v
	$(CLASP) -v
h:
	$(GRINGO) -h
	$(CLASP) -h
