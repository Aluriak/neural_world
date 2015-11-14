"""
Particular default values of the simulation are put here.

"""

import neural_world.commons as commons
from neural_world.commons import Direction, NeuronType
from neural_world.neighbors import moore


# Individual constants
INPUT_NEURON_COUNT  = 16
INPUT_NEURON_TYPE   = NeuronType.INPUT
OUTPUT_NEURON_COUNT = len(Direction)
OUTPUT_NEURON_TYPE  = NeuronType.OR
INDIVIDUAL_INITIAL_COUNT = 4
INDIVIDUAL_INITIAL_DENSITY = None  # use count, not density
# Individual creation values
NEURON_INTER_MINCOUNT = 1
NEURON_INTER_MAXCOUNT = 20
NEURON_EDGES_MINCOUNT = 1
NEURON_EDGES_MAXCOUNT = 20

# Global Life
LIFE_DIVISION_MIN_ENERGY = 20

# Nutrient constants
NUTRIENT_ENERGY = 4
NUTRIENT_REGENERATION = 0.001
NUTRIENT_INITIAL_DENSITY = 0.6

# World space constants and refs
NEIGHBOR_ACCESS = moore
SPACE_WIDTH = 20
SPACE_HEIGHT = 20

if NEIGHBOR_ACCESS is moore:
    assert NEIGHBOR_ACCESS is moore and INPUT_NEURON_COUNT == 16

# Evolution constants
MUTATION_RATE = 0.01
