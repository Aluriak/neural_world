"""
Assume the production of Individual instances.

"""
import random
from random import randint
from functools import partial

import neural_world.config as config
from neural_world.commons    import NeuronType
from neural_world.individual import Individual


class Incubator:
    """Spawn Individual instances"""

    def __init__(self):
        pass

    def spawn(self):
        nb_neuron = randint(2, 10)
        total_nb_neuron = sum((
            nb_neuron,
            config.INPUT_NEURON_COUNT,
            config.OUTPUT_NEURON_COUNT
        ))
        types = (random.choice(tuple(NeuronType.xano()))
                 for _ in range(nb_neuron))
        random.neuron_id = partial(randint, 1, total_nb_neuron+1)
        edges = (
            (random.neuron_id(), random.neuron_id())
            for _ in range(randint(nb_neuron, nb_neuron*4))
        )

        return Individual(
            nb_intermediate_neuron=nb_neuron,
            neuron_types=types,
            edges=edges,
            energy=10,
        )
