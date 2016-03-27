"""
Solving functions for neural network exploitation.

"""
import os
import random
import itertools
from functools   import partial
from collections import deque

from neural_world import default
from neural_world import atoms
from neural_world import commons
from neural_world import solving
from neural_world.commons import (FILE_ASP_RUNNING, FILE_ASP_CLEANING,
                                  NeuronType, Direction)


LOGGER = commons.logger(commons.SUBLOGGER_LIFE)


def square_to_input_neurons(square):
    """From a set of objects, return states of associated input neurons

    square: set of objects (Nutrient, Individual).
    return: 2-tuple of boolean, that are the states of
            input neurons for given square.

    """
    empty = len(square) == 0
    if empty:
        contains_nutrients, contains_individuals = False, False
    else:
        contains_nutrients = any(o.is_nutrient for o in square)
        contains_individuals = any(o.is_individual for o in square)
    return contains_nutrients, contains_individuals


class NeuralNetwork:
    """Encapsulation of many routines about the simple neural network string.

    Each NeuralNetwork instance figure a set of atoms, and provides an API for
    building new NeuralNetwork, reacting to neighbors states and cloning.

    """
    def __init__(self, nb_inter_neuron:int, edges:iter, neuron_types:iter,
                 nb_input_neuron:int=default.INPUT_NEURON_COUNT,
                 nb_output_neuron:int=default.OUTPUT_NEURON_COUNT):
        # Management of neural network data
        self.nb_intermediate_neuron = nb_inter_neuron
        self.nb_input_neuron = nb_input_neuron
        self.nb_output_neuron = nb_output_neuron
        self.edges = tuple(edges)
        self.neuron_types = tuple(neuron_types)
        neuron_type = (_ for _ in self.neuron_types)  # generator
        # generator of neuron id, exhausted when no remaining neurons
        neuron_ids = (idx + 1 for idx in range(self.nb_neuron))
        # Construction of the neural network
        network_atoms = '.'.join(itertools.chain(
            # input neurons
            ('neuron(' + str(idn) + ','
             + default.INPUT_NEURON_TYPE.value + ')'
             for idn in itertools.islice(neuron_ids, 0, nb_input_neuron)),
            # intermediate neurons
            ('neuron(' + str(idn) + ',' + next(neuron_type).value + ')'
             for idn in itertools.islice(neuron_ids, 0, nb_inter_neuron)),
            # # output neurons: give their type and their output status.
            ('neuron(' + str(idn) + ',' + next(neuron_type).value + ').'
             + 'output(' + str(idn) + ',{})'  # this neuron is an output
             for idn in neuron_ids),
            # edges
            ('edge(' + str(id1) + ',' + str(id2) + ')'
             for id1, id2 in self.edges)
        )).format(*Direction.names()) + '.'
        assert network_atoms.count('neuron') == self.nb_neuron
        assert network_atoms.count('edge') == len(self.edges)
        # Cleaning, for remove useless data
        self.neural_network_all = network_atoms
        self.neural_network = NeuralNetwork.cleaned(network_atoms)
        if len(self.neural_network) > 0:
            assert self.neural_network[-1] == '.'


    @property
    def nb_neuron(self):
        """Return the total number of neuron"""
        return (self.nb_intermediate_neuron
                + self.nb_input_neuron
                + self.nb_output_neuron)


    def react(self, states:iter) -> tuple:
        """Return self response to given input neuron states.

        states: iterable of booleans, giving the state of input neurons.
        return: tuple of directions, result of reaction to environment.

        """
        # Atoms creation:
        #  - define the neural network
        #  - add an atom up/1 or down/1 foreach input neuron according to its state
        input_atoms = self.neural_network + ''.join(
            ('up' if is_up else 'down') + '(' + str(neuron) + ').'
            # position in list gives the neuron id
            for neuron, is_up in enumerate(states)
        )
        LOGGER.debug('INPUT ATOMS: "' + input_atoms + '"')
        # ASP solver call
        model = solving.model_from(input_atoms, FILE_ASP_RUNNING)
        LOGGER.debug('OUTPUT ATOMS: ' + str(model))
        # Directions of movement extraction: get id of up-state output neurons
        directions = (Direction[atoms.arg(atom)] for atom in model
                      if atom.startswith('direction('))
        return tuple(Direction.simplified(directions))


    def clone(self, mutator=None):
        """Return a copy of self, eventually mutated by given mutator"""
        # copy the data, mutate it if any mutator given
        nb_intermediate_neuron, neuron_types = (self.nb_intermediate_neuron,
                                                self.neuron_types)
        edges = self.edges
        if mutator:
            nb_intermediate_neuron, neuron_types, edges = mutator.mutate(
                self.nb_intermediate_neuron, self.nb_neuron,
                self.neuron_types, self.edges
            )

        return NeuralNetwork(
            edges=edges,
            nb_inter_neuron=nb_intermediate_neuron,
            neuron_types=neuron_types,
            nb_input_neuron=self.nb_input_neuron,
            nb_output_neuron=self.nb_output_neuron,
        )



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
