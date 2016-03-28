"""
Assume the production of Individual instances.

"""
import random
from random import randint
from functools import partial

import neural_world.default as default
from neural_world.commons    import NeuronType
from neural_world.individual import Individual
from neural_world.commons    import Configurable
from neural_world.neural_network import NeuralNetwork


class Incubator(Configurable):
    """Spawn Individual instances"""

    def __init__(self, config):
        super().__init__(config=config, config_fields=[
            'memory_min_size', 'memory_max_size',
            'neuron_inter_mincount', 'neuron_inter_maxcount',
            'neuron_edges_mincount', 'neuron_edges_maxcount',
            'neuron_input_count', 'neuron_output_count',
            'mutator',
        ])
        self.neuron_types = NeuronType.ixano()


    def spawn(self):
        """Spawn Individual instances"""
        # get data & shortcuts
        nb_inter_neuron = randint(self.neuron_inter_mincount,
                                  self.neuron_inter_maxcount)
        memory_size = randint(self.memory_min_size,
                              self.memory_max_size)
        nb_neuron = self.neuron_total_count(nb_inter_neuron, memory_size)
        random.neuron_id = partial(randint, 1, nb_neuron)
        # neuron types and edges random generation
        neuron_types = (
            random.choice(self.neuron_types)
            for _ in range(self.neuron_type_total_count(nb_inter_neuron,
                                                        memory_size))
        )
        edges = (
            (random.neuron_id(), random.neuron_id())
            for _ in range(randint(self.neuron_edges_mincount,
                                   self.neuron_edges_maxcount))
        )

        # Construction of the neural network
        neural_network = NeuralNetwork(
            edges=edges,
            nb_inter_neuron=nb_inter_neuron,
            memory_size=memory_size,
            nb_input_neuron=self.neuron_input_count,
            nb_output_neuron=self.neuron_output_count,
            neuron_types=neuron_types,
        )

        # Spawn of the individual itself
        return Individual(
            neural_network=neural_network,
            energy=10,
        )


    def clone(self, indiv, energy=None):
        """Clone given individual, and apply self mutator on clone, which will
        get the given energy.

        If energy is None, half of the energy keeped by self will be given
        to the new clone.

        """
        return indiv.clone(self.mutator, energy)


    def neuron_total_count(self, nb_intermediate_neuron, memory_size):
        """Return the total number of neuron present in an individual
        with given number of intermediate neuron."""
        return NeuralNetwork.neuron_total_count(nb_intermediate_neuron,
                                                memory_size,
                                                self.neuron_input_count,
                                                self.neuron_output_count)


    def neuron_type_total_count(self, nb_intermediate_neuron, memory_size):
        """Return the total number of needed neuron type"""
        return NeuralNetwork.neuron_type_total_count(nb_intermediate_neuron,
                                                memory_size,
                                                self.neuron_input_count,
                                                self.neuron_output_count)
