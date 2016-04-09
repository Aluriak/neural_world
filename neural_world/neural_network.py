"""
Solving functions for neural network exploitation.

"""
import os
import random
import itertools
from functools   import partial
from collections import deque

from neural_world import actions
from neural_world import default
from neural_world import atoms
from neural_world import commons
from neural_world import solving
from neural_world.commons import (FILE_ASP_RUNNING, FILE_ASP_CLEANING,
                                  NeuronType, Direction)
from neural_world.neural_network_engine import NeuralNetworkEngine, MINIMAL_NEURON_ID


LOGGER = commons.logger(commons.SUBLOGGER_LIFE)


class NeuralNetwork(NeuralNetworkEngine):
    """Definition of the neural network behaviors.

    About the memory:

    The input memory neurons are named input because they inject
    the memory value inside the network.
    The output memory neurons are named output because they are output
    of the neural running.

    When the neural network is ran, memory input neurons are mapped to up
    or down accordingly to the memory values.
    When an output memory neuron is up after the run, the memory value at the
    associated address is inverted (True <-> False).

    """
    from collections import Counter
    DIRECTIONS = Counter()
    MEMORIES = Counter()
    MINIMAL_NEURON_ID = MINIMAL_NEURON_ID

    def __init__(self, nb_inter_neuron:int, memory_size:int,
                 nb_neighbor:int=default.NEIGHBOR_COUNT,
                 nb_unit_type:int=default.UNIT_TYPE_COUNT, **kwargs):
        # shortcuts
        nb_neighbor_neuron = NeuralNetwork.nb_neighbor_neuron(nb_neighbor, nb_unit_type)
        # fields and finally a call to base class init
        self.memory = [False] * memory_size
        self.energy_level_precision = 5
        self.max_energy = 0
        super().__init__(inputs=((self.neighbors, nb_neighbor_neuron),
                                 (self.read_memory, self.memory_size),
                                 (self.energy_level, self.energy_level_precision)),
                         outputs=((self.directions, len(Direction)),
                                  (self.write_memory, self.memory_size),
                                  (self.replication, 1),
                                  (self.reproduction, 1)),
                         nb_intermediate_neuron=nb_inter_neuron, **kwargs)


    def neighbors(self, **kwargs):
        return tuple(itertools.chain.from_iterable(
            NeuralNetwork.square_to_input_neurons(square)
            for square in kwargs['neighbors']
        ))

    def directions(self, states, **kwargs):
        directions = tuple(d for s, d in zip(states, Direction) if s)
        NeuralNetwork.DIRECTIONS.update(directions)
        yield actions.MoveAction(kwargs['individual'], kwargs['coords'], directions)


    def energy_level(self, individual, **kwargs):
        """Define a fixed set of neurons, giving information of percentage
        of energy level.
        The closer to the maximal amount of energy, the bigger is the number
        of returned up states.

        The maximal amount of energy equals to the maximal energy value
        encountered by the neural network.

        """
        self.max_energy = max(self.max_energy, individual.energy)
        percent = int(individual.energy // self.max_energy * 100) // self.energy_level_precision
        levels = tuple(n * (self.max_energy // self.energy_level_precision)
                  for n in range(0, self.energy_level_precision))
        return tuple(percent >= level for level in levels)


    def read_memory(self, **kwargs):
        return self.memory

    def write_memory(self, states, **kwargs):
        """Change the memory, according to given states"""
        assert len(states) == len(self.memory)
        # if a state is True, the associated value in memory is changed:
        # Memory values:    0 1 0 1
        # States values:    0 0 1 1    < this is XOR !
        # New memory   :    0 1 1 0
        # Consequence: (memory xor states) -> new memory
        self.memory = [v != s for s, v in zip(states, self.memory)]
        NeuralNetwork.MEMORIES.update(i for i, s in enumerate(states) if s)
        yield

    @property
    def memory_size(self):
        return len(self.memory)


    def replication(self, states, individual, coords, **kwargs):
        """Only one neuron ; if activated, the individual will
        seek to clone itself."""
        assert len(states) == 1
        if states[0] and individual.energy >= default.LIFE_DIVISION_MIN_ENERGY:
            yield actions.ReplicateAction(individual, coords)


    def reproduction(self, states, individual, coords, **kwargs):
        """Only one neuron ; if activated, the individual will
        seek to clone itself."""
        assert len(states) == 1
        if states[0] and individual.energy >= default.LIFE_DIVISION_MIN_ENERGY:
            yield actions.ReplicateAction(individual, coords)


    @classmethod
    def nb_neighbor_neuron(cls, nb_neighbor=default.NEIGHBOR_COUNT,
                           nb_type=default.UNIT_TYPE_COUNT):
        return nb_type * nb_neighbor


    @staticmethod
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


    def clone(self, mutator=None):
        """Return a copy of self, eventually mutated by given mutator"""
        # copy the data, mutate it if any mutator given
        nb_intermediate_neuron= self.nb_intermediate_neuron
        neuron_types = self.neuron_types
        edges = self.edges

        if mutator:
            nb_intermediate_neuron, neuron_types, edges = mutator.mutate(
                self.nb_intermediate_neuron, self.nb_neuron,
                self.neuron_types, self.edges
            )

        return NeuralNetwork(
            edges=edges, neuron_types=neuron_types,
            memory_size=self.memory_size,
            nb_inter_neuron=nb_intermediate_neuron,
        )
