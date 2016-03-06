import unittest
from neural_world.commons import NeuronType


class TestEnumNeuronType(unittest.TestCase):

    def test_accessors(self):
        for accessor in (NeuronType.xano, NeuronType.ixano, NeuronType.ixanom):
            self.assertEqual(
                ''.join(e.value for e in accessor()),
                accessor.__name__
            )
