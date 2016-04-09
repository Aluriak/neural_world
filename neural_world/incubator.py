"""
Assume the production of Individual instances.

"""
import random
from functools import partial

import neural_world.default as default
from neural_world.commons    import NeuronType
from neural_world.individual import Individual
from neural_world.commons    import Configurable
from neural_world.neural_network import NeuralNetwork


class Incubator(Configurable):
    """Spawn Individual instances.

    A simple way to create a new Incubator behavior is to subclass Incubator,
    and redefine the following methods: memory_size,
    nb_inter_neuron, nb_edges, random_neuron_id.

    """

    def __init__(self, config):
        super().__init__(config=config, config_fields=[
            'memory_min_size', 'memory_max_size',
            'neuron_inter_mincount', 'neuron_inter_maxcount',
            'neuron_edges_mincount', 'neuron_edges_maxcount',
            'mutator',
        ])
        self.neuron_types = NeuronType.xano()


    def memory_size(self):
        """Return the memory size"""
        return random.randint(self.memory_min_size, self.memory_max_size)

    def nb_inter_neuron(self):
        """Return number of intermediate neuron"""
        return random.randint(self.neuron_inter_mincount, self.neuron_inter_maxcount)

    def nb_edges(self):
        """Return number of edges"""
        return random.randint(self.neuron_edges_mincount, self.neuron_edges_maxcount)

    def random_neuron_type(self):
        """Return a random neuron type"""
        return random.choice(self.neuron_types)


    def spawn(self):
        """Spawn Individual instances"""
        # Construction of the neural network
        neural_network = NeuralNetwork(
            nb_inter_neuron=self.nb_inter_neuron(),
            memory_size=self.memory_size(),
        )
        nb_neuron_type = neural_network.nb_neuron_type
        random.nid = lambda: (random.randint(NeuralNetwork.MINIMAL_NEURON_ID,
                                             neural_network.nb_neuron))
        random.eid = lambda: (random.nid(), random.nid())
        neural_network.build(
            edges=(random.eid() for _ in range(self.nb_edges())),
            neuron_types=(self.random_neuron_type() for _ in range(nb_neuron_type))
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
