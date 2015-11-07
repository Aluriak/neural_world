"""
Particular values of the simulation are put here.

"""

import neural_world.commons as commons
from neural_world.commons import Direction, NeuronType
from neural_world.neighbors import moore


# Individual constants
INPUT_NEURON_COUNT  = 16
INPUT_NEURON_TYPE   = NeuronType.INPUT
OUTPUT_NEURON_COUNT = len(Direction)
OUTPUT_NEURON_TYPE  = NeuronType.OR

# World space constants and refs
NEIGHBOR_ACCESS = moore

if NEIGHBOR_ACCESS is moore:
    assert NEIGHBOR_ACCESS is moore and INPUT_NEURON_COUNT == 16
