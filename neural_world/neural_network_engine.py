"""Definition of the NeuralNetworkEngine base class."""

import itertools

from neural_world import commons
from neural_world import default
from neural_world import solving
from neural_world.commons import (NeuronType, Direction,
                                  FILE_ASP_CLEANING, FILE_ASP_RUNNING)


LOGGER = commons.logger(commons.SUBLOGGER_LIFE)
MINIMAL_NEURON_ID = 1


class NeuralNetworkEngine:
    """Base class for the NeuralNetwork class. Define the underlying behavior
    of neural networks, as an abstract object.

    Each neural network figures a set of atoms, and provides an API for
    building new neural networks, reacting to neighbors states and cloning.

    A neural network is a string, containing ASP-formatted data as atoms as:
        - neuron(I,T): neuron of id I is of type T (T in IXANO)
        - output(I): neuron of id I is an output neuron
        - edge(I,J): there is an edge between neurons of id I and J


    The object assume that inputs and outputs attributes are iterables
    of pairs (f, n), where f is a function and n the number of neuron
    associated to the function.
    For input neurons, function takes no parameters, and should return
    an iterable of n boolean values.
    For output neurons, function receive an iterable of n boolean values,
    and can yield Action.

    Subclasses of NeuralNetworkEngine should define the content of inputs
    and outputs, and expose them through the NeuralNetworkEngine.__init__ method.

    """

    def __init__(self, nb_intermediate_neuron:int, inputs:tuple, outputs:iter,
                 edges:iter=None, neuron_types:iter=None):
        self.inputs, self.outputs = tuple(inputs), tuple(outputs)
        self.nb_intermediate_neuron = nb_intermediate_neuron
        self._nb_input_neuron = sum(int(n) for _, n in self.inputs)
        self._nb_output_neuron = sum(int(n) for _, n in self.outputs)
        if edges is not None and neuron_types is not None:
            self.build(edges, neuron_types)
        else:
            self.edges, self.neuron_types = None, None  # build() call necessary

    def build(self, edges:iter, neuron_types:iter):
        """Build the neural network using input data and attributes"""
        self.edges, self.neuron_types = tuple(edges), tuple(neuron_types)

        neuron_ids = iter(range(MINIMAL_NEURON_ID, self.nb_neuron + MINIMAL_NEURON_ID))
        neuron_type = iter(self.neuron_types)
        network_atoms = '.'.join(itertools.chain(
            # input neurons
            ('neuron(' + str(idn) + ','
             + default.INPUT_NEURON_TYPE.value + ')'
             for idn in itertools.islice(neuron_ids, 0, self.nb_input_neuron)),
            # intermediate neurons
            ('neuron(' + str(idn) + ',' + next(neuron_type).value + ')'
             for idn in itertools.islice(neuron_ids, 0, self.nb_intermediate_neuron)),
            # output neurons: give their type and their output status.
            ('neuron(' + str(idn) + ',' + next(neuron_type).value + ').'
             + 'output(' + str(idn) + ')'  # this neuron is an output
             for idn in neuron_ids),
            # edges
            ('edge(' + str(id1) + ',' + str(id2) + ')'
             for id1, id2 in self.edges)
        )) + '.'
        assert network_atoms.count('neuron') == self.nb_neuron
        assert network_atoms.count('edge') == len(self.edges)
        assert network_atoms.count('output') == self.nb_output_neuron
        assert network_atoms.count(',i)') == self.nb_input_neuron
        assert ('neuron(' + str(MINIMAL_NEURON_ID)) in network_atoms
        assert ('neuron(' + str(self.maximal_neuron_id)) in network_atoms
        assert ('neuron(' + str(MINIMAL_NEURON_ID-1)) not in network_atoms
        # Cleaning, for remove useless data
        self.neural_network_all = network_atoms
        self.neural_network = NeuralNetworkEngine.cleaned(network_atoms)
        LOGGER.debug('NEW NEURAL NETWORK: ' + self.neural_network_all)
        LOGGER.debug('CLEANED: ' + self.neural_network)

    def input_states(self, kwargs):
        for input_func, nb_neuron in self.inputs:
            states = input_func(**kwargs)
            assert len(states) == nb_neuron
            yield from states

    def react(self, **kwargs):
        """Call all output functions, based on reactions of the neural network
        to input functions, and yield their results."""
        self.reaction_data = kwargs
        output_states = self.output_from(self.input_states(kwargs))
        assert self.nb_output_neuron == len(output_states)
        output_states = iter(output_states)
        for output_func, values in self.outputs:
            yield from output_func(tuple(itertools.islice(output_states, 0, values)),
                                   **kwargs)


    def output_from(self, input_states:iter) -> tuple:
        """Return output states responding to given input neuron states.

        states: iterable of booleans, giving the state of input neurons.
        return: iterable of booleans, giving the state of output neurons.

        """
        # Atoms creation:
        #  - define the neural network
        #  - add an atom up/1 or down/1 foreach input neuron according to its state
        input_atoms = self.neural_network + ''.join(
            'up(' + str(idn) + ').'
            # position in list gives the input neuron id
            for idn, is_up in enumerate(input_states, start=MINIMAL_NEURON_ID)
            if is_up
        )
        LOGGER.debug('INPUT ATOMS: "' + input_atoms + '"')
        # ASP solver call
        model = solving.model_from(input_atoms, FILE_ASP_RUNNING)
        LOGGER.debug('OUTPUT ATOMS: ' + str(model))
        up_outputs = set(int(atom.split('(')[1].strip(')'))
                         for atom in model if atom.startswith('up'))
        min_output_neuron_id = self.min_output_neuron_id
        ret = tuple(idx in up_outputs for idx in range(min_output_neuron_id,
                                                       self.maximal_neuron_id+1))
        LOGGER.debug('OUTPUT STATES: ' + str(ret))
        return ret

    @property
    def maximal_neuron_id(self):
        return sum((
            self.nb_input_neuron,
            self.nb_intermediate_neuron,
            self.nb_output_neuron,
        ))

    @property
    def nb_input_neuron(self):
        return self._nb_input_neuron

    @property
    def nb_output_neuron(self):
        return self._nb_output_neuron

    @property
    def nb_neuron(self):
        """Return the total number of neuron"""
        return NeuralNetworkEngine.neuron_total_count(
            self.nb_intermediate_neuron,
            self.nb_input_neuron,
            self.nb_output_neuron
        )

    @property
    def min_output_neuron_id(self):
        return self.nb_neuron - self.nb_output_neuron + MINIMAL_NEURON_ID

    @staticmethod
    def neuron_type_total_count(nb_intermediate, nb_output):
        """Return the total number of needed neuron XANO type"""
        return sum((nb_intermediate, nb_output))

    @property
    def nb_neuron_type(self):
        return NeuralNetworkEngine.neuron_type_total_count(self.nb_intermediate_neuron,
                                                           self.nb_output_neuron)

    @staticmethod
    def neuron_total_count(nb_inter, nb_input, nb_output):
        """Return the total number of neuron present in an individual"""
        return sum((nb_input, nb_inter, nb_output))


    @staticmethod
    def cleaned(network_atoms:str) ->str:
        """Return a cleaned version of given neural network to remove
        useless neuron, give an orientation to edges,..."""
        model = solving.model_from(network_atoms, FILE_ASP_CLEANING)
        assert model is not None, 'cleaning network lead to non existing model'
        return '.'.join(model) + ('.' if len(model) else '')


    @staticmethod
    def from_string(atoms, nb_neuron:int=None, nb_input=None, nb_output=None,
                    neuron_types=NeuronType.ixano):
        """Return a new NeuralNetwork instance, initialized from given
        string of atoms.
        Note that all the field may be badly initialized."""
        if nb_neuron is None:
            nb_neuron = atoms.count('neuron')
        if nb_output is None:
            nb_output = atoms.count('output')
        if nb_input is None:
            nb_input = atoms.count(',' + NeuronType.INPUT.value + ')')
        nb_inter = nb_neuron - nb_output - nb_input
        instance = NeuralNetwork((), nb_inter, nb_input,
                                 nb_output, neuron_types)
        instance.neural_network = atoms
        return instance


    def __str__(self):
        return self.neural_network
