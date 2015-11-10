"""
Definition of the NeuronType enumeration.

"""
from enum import Enum


class NeuronType(Enum):
    """Type of a Neuron is in IXANO"""
    INPUT = 'i'
    XOR   = 'x'
    AND   = 'a'
    NOT   = 'n'
    OR    = 'o'

    @staticmethod
    def ixano(): return tuple(e for e in NeuronType)
    @staticmethod
    def xano(): return tuple(e for e in NeuronType
                             if e is not NeuronType.INPUT)

assert ''.join(e.value for e in NeuronType.ixano())== NeuronType.ixano.__name__
assert ''.join(e.value for e in NeuronType.xano()) == NeuronType.xano.__name__
