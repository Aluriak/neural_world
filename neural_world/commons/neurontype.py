"""
Definition of the NeuronType enumeration.

"""
from enum import Enum


class NeuronType(Enum):
    """Type of a Neuron is in XANO, IXANO or IXANOJP"""
    INPUT, XOR, AND, NOT, OR = 'ixano'
    INPUT_MEMORY, OUTPUT_MEMORY = 'jp'

    @staticmethod
    def ixanojp(): return tuple(e for e in NeuronType)

    @staticmethod
    def ixano():
        return (NeuronType.INPUT,
                NeuronType.XOR, NeuronType.AND,
                NeuronType.NOT, NeuronType.OR)

    @staticmethod
    def xano():
        return (NeuronType.XOR, NeuronType.AND,
                NeuronType.NOT, NeuronType.OR)
