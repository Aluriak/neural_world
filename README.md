# Neural World
Binary neural networks playing in a 2D world, implemented in Python and Answer Set Programming.


## Principles
Each individual in the simulated world have a *Binary Neural Networks* (see after for details), and an amount of energy.
The BNN gives, for each configuration of the moore neighbors, a direction of propagation, allowing individuals to move according
to the configuration of their immediate environnement.

Another element, nutrients, appears randomly in the world, and can be consummed by individuals for get some energy.
Detection of nutrients and other individuals is perform through the BNN, so a good BNN can lead to smart reactions to environnement composition.

As the BNN are generated randomly and randomly mutated when they divides themselves, the individuals are under evolution.
Moreover, individuals, when they reach 0 of energy, dies and disappears. Here is for the selection.


## Usage
Simpler way to use Neural World currently is:

    make

It will show a little world with some life in it, then ask you something to do through a basical prompt. (type *help* for help)

Once you have failed to do something useful with that, you can:
- see the logs, in *neural_world/logs/*, because you love the logs;
- see the archives of your run, in *neural_world/archives/*, and look at all the graphs generated representing the neural networks in png;
- see the ASP code in *neural_world/asp/*, and notice the ridiculous number of LOC necessary for play with BNN;
- look at the *neural_world/actions.py* source file. Its high-level and give a good look to the global program actions;
- look at the *neural_world/engine.py* source file, where the main loop of step is designed;
- look at the *neural_world/__main__.py* source file, where global behavior of the program is defined (see *next steps* part);
- look at the *neural_world/neural_network.py* source file, where all the logic about BNN is implemented;
- create your own observer, that do lots of things (opengl representation, real-time statistical analysis,…);


Soon, an individual-centered mode will be implemented:

    make indiv


### Archives
Are Generated archives for each run performed, thanks to the *Archivist* observer of World.
By default, the Archivist directly compiles [dot data](https://en.wikipedia.org/wiki/DOT_%28graph_description_language%29)
through [pygraphviz](http://graphviz.org/) module, and render all graphs in dedicated PNG pictures.
This behavior can be changed, in order to get a quicker simulation computation, with the command line interface.


## Installation
First, some Python modules need to be installed, including [docopt](http://docopt.org), [pyasp](http://github.com/sthiele/pyasp),
[prompt-toolkit](https://github.com/jonathanslenders/python-prompt-toolkit) and [pygraphviz](https://github.com/pygraphviz/pygraphviz):

    pip install -r requirements


## Next steps
### Simulation
- [X] basic unit tests about the solving, the logic part and some details;
- [X] memory implementation (each individual have its own memory, and can play with it);
- [ ] basic unit tests about the Individual class;
- [ ] implement communication between individuals (input neuron take its value from output neuron of neighbor individual);
- [ ] turn binary neural network in discrete neural network (use of integer instead of True/False);
- [ ] use [ACCC](https://github.com/Aluriak/ACCC) for create neural networks and perform the mutations;
- [ ] add some basical command line arguments: (automatically creat neural network rendering, for example);
- [ ] rewrite the main for support user configurations and embedding;
- [ ] do something cool with the Nutrient concept (game of life populating ? Evolution capabilities ?);
- [ ] improve genealogic tree outputs;
- [ ] encapsulate the main current sequence inside an object that incite user to create his own sequence;

### Individual Simulation
- [ ] basical prompt for modifying parameters and BNN;
- [ ] visualization of the BNN through [tergraw](http://github.com/aluriak/tergraw);
- [ ] visualization and modification of neighborood;
- [ ] visualization and modification of memory;


## Binary Neural Networks definition
Binary neural networks have three group of neurons:
- input neurons, two per neighbor square in the simulated world, giving informations about presence and absence of elements.
- output neurons, four, one for each possible direction of propagation.
- intermediate neurons, variable in number and type, can be considered as logical gates (XOR, AND, NOT, OR).
- memory neurons, dissociated in reading (input) and writing (output) neurons, allowing the neural network to use its memory.

Moreover, there is edges between neurons that perform the signal linking.

When an output neuron is in up state, the associated direction will be used for determine how the individual will move.
When a writing memory neuron is up state, the associated address in memory will be swaped. (True become False, vice-versa)
Reading memory neurons are each associated to an address in memory, and equal to the value found at this address.


The network resolution is performed through [Answer Set Programming](https://en.wikipedia.org/wiki/Answer_set_programming)
and particularly the [pyasp](https://pypi.python.org/pypi/pyasp/) module, that perform the interface between Python and ASP.
See installation part for details and help.
Note that the network is never stocked by Python in other way than strings containing atoms, as all treatments on the networks are perform with ASP.


## Architecture
- Individual: life unit, that have a NeuralNetwork and energy.
- NeuralNetwork: definition of BNN, with all the associated primitives.
- Direction: enumeration highly giving the four directions in a 2D world.
- NeuronType: enumeration of the 5 types of neurons, which are Input, Xor, And, Not and Or, abbreviated IXANO.
- Incubator: factory of individuals.
- Mutator: modifier of NeuralNetwork property.
- Actions: commands created by individuals, GUI and even commands, applicated later by the engine on the world.
- World: built on top of the space definition, provides a complete API for modify the simulation.
- Engine: invoker of commands on the world.
- WorldView: observer of world, printing things in the terminal.
