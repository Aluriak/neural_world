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


class Incubator(Configurable):
    """Spawn Individual instances"""

    def __init__(self, config):
        super().__init__(config=config, config_fields=[
            'neuron_inter_mincount', 'neuron_inter_maxcount',
            'neuron_edges_mincount', 'neuron_edges_maxcount',
            'mutator',
        ])

    def spawn(self):
        """Spawn Individual instances"""
        # get data & shortcuts
        nb_neuron = randint(self.neuron_inter_mincount,
                            self.neuron_inter_maxcount)
        total_nb_neuron = Individual.neuron_total_count(nb_neuron)
        random.neuron_id = partial(randint, 1, total_nb_neuron + 1)
        # types and edges random generation
        types = (random.choice(tuple(NeuronType.xano()))
                 for _ in range(nb_neuron))
        edges = (
            (random.neuron_id(), random.neuron_id())
            for _ in range(randint(self.neuron_edges_mincount,
                                   self.neuron_edges_maxcount))
        )

        return Individual(
            nb_intermediate_neuron=nb_neuron,
            neuron_types=types,
            edges=edges,
            energy=10,
        )

    def clone(self, indiv, energy=None):
        """Clone given individual, and apply self mutator on clone, which will
        get the given energy.

        If energy is None, half of the energy keeped by self will be given
        to the new clone.

        """
        return indiv.clonage(self.mutator, energy)
