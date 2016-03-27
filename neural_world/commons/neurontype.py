"""
Definition of the NeuronType enumeration.

"""
from enum import Enum


class NeuronType(Enum):
    """Type of a Neuron is in IXANO"""
    INPUT, XOR, AND, NOT, OR = 'ixano'

    @staticmethod
    def ixano(): return tuple(e for e in NeuronType)

    @staticmethod
    def xano(): return tuple(e for e in NeuronType if e is not NeuronType.INPUT)
