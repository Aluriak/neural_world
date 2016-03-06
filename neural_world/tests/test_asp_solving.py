"""
Unit tests for ASP solving.

"""

import unittest
from collections import defaultdict

from neural_world.neural_network import model_from, FILE_ASP_SOLVING


class SolvingTester(unittest.TestCase):
    """Mother class of all next classes.

    Defines the assert_solving function, designed as high level ASP output test.

    """

    def assert_solving(self, atoms, expected_result):
        solved = self._solve(atoms)
        expected = self._uniformized(expected_result)
        # debug printings
        # print('\n\tATOMS   : ' + atoms,
              # '\n\tFOUND   : ' + solved,
              # '\n\tEXPECTED: ' + expected,
              # '\n\tEQUALITY: ' + str(expected == solved))
        self.assertEqual(solved, expected)

    def _solve(self, atoms):
        """Return model found with given program and atoms, uniformized"""
        return self._uniformized(model_from(atoms, FILE_ASP_SOLVING))

    def _uniformized(self, model):
        """Return given atoms, uniformized and then, comparable"""
        try:
            return '.'.join(sorted(atom for atom in model))
        except TypeError:  # no model found
            return ''


class TestASPSolving(SolvingTester):

    def test_no_atoms(self):
        atoms = ''
        expected_result = ()
        self.assert_solving(atoms, expected_result)

    def test_two_neurons_down(self):
        atoms = 'neuron(1,i). neuron(2,o). output(2,up).'
        expected_result = ()
        self.assert_solving(atoms, expected_result)

    def test_two_neurons_up(self):
        atoms = 'neuron(1,i). neuron(2,o). output(2,up). up(1). edge(1,2).'
        expected_result = ('direction(up)',)
        self.assert_solving(atoms, expected_result)

    def test_three_neurons_up(self):
        atoms = ('neuron(1,i). neuron(2,i). neuron(3,a). output(3,left). '
                 'up(1). up(2). edge(1,3). edge(2,3).')
        expected_result = ('direction(left)',)
        self.assert_solving(atoms, expected_result)

    def test_two_paths(self):
        """Test on a complex network.

            1 --> 3 (NOT) ->\
             \               6 (XOR, down)
              4 (OR) ------->|
             /               7 (AND, right)
            2 --> 5 (NOT) ->/

        All cases of input states (none, up 1, up 2, up 1 & up 2) are tested.

        """
        atoms = ('neuron(1,i). neuron(2,i). '  # two input neurons
                 'neuron(3,n). neuron(4,o). neuron(5,n). '  # (not, or, not) neurons
                 'neuron(6,x). output(6,down). neuron(7,a). output(7,right). '  # (xor, and) output neurons
                 'edge(1,3). edge(1,4). edge(2,4). edge(2,5). '
                 'edge(3,6). edge(4,6). edge(4,7). edge(5,7). ')
        expected_results = {  # up states: expected result
            ''             : ('direction(down)',),
            'up(1).'       : ('direction(down)', 'direction(right)'),
            'up(2).'       : (),
            'up(1).up(2).' : ('direction(down)',),
        }
        for up_states, expected_result in expected_results.items():
            self.assert_solving(atoms + up_states, expected_result)


class TestNeuronLogicalGates(SolvingTester):
    """Test all logical gates, with all possible cases of
    predecessor neurons states.

    """
    def setUp(self):
        """Create three input neurons, predecessors of a single neuron and all
        possible cases of input."""
        self.atoms = ('neuron(1,i). neuron(2,i). neuron(3,i).'
                      'neuron(4,{}). output(4,left).'  # neuron 4 will be tested with all possible gates
                      'edge(1,4). edge(2,4). edge(3,4).')
        self.cases = {  # {input states: {gate: activated direction expected}}
            ''                  : {'not'},
            'up(1).'            : {'or', 'xor'},
            'up(2).'            : {'or', 'xor'},
            'up(3).'            : {'or', 'xor'},
            'up(1).up(2).'      : {'or'},
            'up(1).up(3).'      : {'or'},
            'up(2).up(3).'      : {'or'},
            'up(1).up(2).up(3).': {'or', 'and'},
        }

    def test_gates(self):
        """Test for all gates all cases of up states, and verify that all
        results match with the expected ones."""
        for gate in ('and', 'or', 'xor', 'not'):
            for states, expected_result in self.cases.items():
                self.assert_solving(
                    self.atoms.format(gate[0]) + states,
                    ('direction(left)',) if gate in expected_result else (),
                )
