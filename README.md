# Neural World
Binary neural networks plays in a 2D world, implemented in Python and Answer Set Programming.

__Not tested in Python 2__



## Principles
Each individual in the simulated world have a Binary Neural Networks (see after for details), and an amount of energy.
The BNN gives, for each configuration of the moore neighbors, a direction of propagation, allowing individuals to move according
to the configuration of their immediate environnement.

Another element, nutrients, appears randomly in the world, and can be consummed by individuals for get some energy.
Detection of nutrients and other individuals is perform through the BNN, so a good BNN can lead to smart reactions to environnement composition.

As the BNN are generated randomly and randomly mutated when they divides themselves, the individuals can evolve.
Moreover, individuals, when they reach 0 of energy, dies and disappears. Here is for the selection.


## Usage
Simpler way to use Neural World currently is:

    make

It will show a little world with some life in it, then ask you something to do through a basical prompt. (type *help* for help)

Once you have failed to do something useful with that, you can:
- see the logs, in *neural_world/logs/*, because you love the logs;
- see the archives of your run, in *neural_world/archives/*, and look at all the graphs generated representing the neural networks in png;
- see the ASP code, and notice the ridiculous number of LOC necessary for play with BNN;
- look at the *neural_world/actions.py* source file. Its high-level and give a good look at the global behavior of the program;
- look at the *neural_world/engine.py* source file, where the main loop of step is designed;
- look at the *neural_world/__main__.py* source file, where global behavior of the program is defined (see *next steps* part);
- create your own observer, that do lots of things;


### Archives
Are Generated archives for each run performed, thanks to the *Archivist* observer of World.
By default, the Archivist directly compiles [dot data]() through [pygraphviz]() module, and render all graphs in dedicated PNG pictures.
This behavior can be changed, in order to get a quicker simulation computation, with the command line interface.


## Installation
First, some Python modules need to be installed, including docopt and pyasp.

    pip install -r requirements

Pyasp needs a configuration. Currently, the only way i know to do that is:
- get compatible versions of [gringo](http://sourceforge.net/projects/potassco/files/gringo/4.5.3/) and [clasp](http://sourceforge.net/projects/potassco/files/clasp/3.1.3/) on the [potassco website](http://sourceforge.net/projects/potassco/files);
- put the retrieved executables __gringo__ and __clasp__ in __/usr/lib/python3.5/site-packages/pyasp/bin__, with names __gringo4__ and __clasp__, respectively;

This manipulation is necessary while pyasp doesn't get the used version of gringo and clasp. (4.5.3 and 3.1.3)
This program is tested with gringo 4.5.1 and 4.5.3, and not compliant with versions 4.4.x, because of some known bugs.


## Next steps
- [ ] implement communication between individuals (input neuron take its value from output neuron of neighbor individual);
- [ ] turn binary neural network in discrete neural network (use of integer instead of True/False);
- [ ] implement individual global states (output neuron gives values for input neurons at next step);
- [ ] use [ACCC](https://github.com/Aluriak/ACCC) for create neural networks and perform the mutations;
- [ ] add some basical command line arguments: (automatically creat neural network rendering, for example);
- [ ] rewrite the main for support user configurations and embedding;
- [ ] do something cool with the Nutrient concept (game of life populating ? Evolution capabilities ?);
- [ ] improve genealogic tree outputs;
- [ ] encapsulate the main current sequence inside an object that incite user to create his own sequence;


## Binary Neural Networks definition
Binary neural networks have three group of neurons:
- input neurons, two per neighbor square in the simulated world, giving informations about presence and absence of elements.
- output neurons, four, one for each possible direction of propagation.
- intermediate neurons, variable in number and type, can be considered as logical gates (XOR, AND, NOT, OR).

Moreover, there is edges between neurons that perform the signal linking.

When an output neuron is in up state, the associated direction will be used for determine how the individual will move.


The network resolution is performed through [Answer Set Programming](https://en.wikipedia.org/wiki/Answer_set_programming)
and particularly the [pyasp](https://pypi.python.org/pypi/pyasp/) module, that perform the interface between Python and ASP.
See installation part for details and help.
Note that the network is never stocked by Python in other way than strings containing atoms, as all treatments on the networks are perform with ASP.


## Architecture
- Individual: life unit, that have a BNN (stocked as a string of atoms dedicated to ASP solver) and energy.
- Direction: enumeration highly giving the four directions in a 2D world.
- NeuronType: enumeration of the 5 types of neurons, which are Input, Xor, And, Not and Or, abbreviated IXANO.
- Incubator: factory of individuals.
- Mutator: modifier of individuals property.
- Actions: commands created by individuals, GUI and even commands, applicated later by the engine on the world.
- World: built on top of the space definition, provides a complete API for modify the simulation.
- Engine: invoker of commands on the world.
- WorldView: observer of world, printing things in the terminal.
