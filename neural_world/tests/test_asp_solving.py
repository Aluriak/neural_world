"""
Unit tests for ASP solving.

"""

import unittest
from collections import defaultdict

from neural_world.tests import NeuralNetworkTester


class TestASPSolving(NeuralNetworkTester):

    def test_no_atoms(self):
        atoms = ''
        expected_result = ''
        self.assert_running(atoms, expected_result)

    def test_two_neurons_down(self):
        atoms = 'neuron(1,i). neuron(2,o). output(2,up).'
        expected_result = ()
        self.assert_running(atoms, expected_result)

    def test_two_neurons_up(self):
        atoms = 'neuron(1,i). neuron(2,o). output(2,up). up(1). edge(1,2).'
        expected_result = ('direction(up)',)
        self.assert_running(atoms, expected_result)

    def test_three_neurons_up(self):
        atoms = ('neuron(1,i). neuron(2,i). neuron(3,a). output(3,left). '
                 'up(1). up(2). edge(1,3). edge(2,3).')
        expected_result = 'direction(left)'
        self.assert_running(atoms, expected_result)

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
            ''             : 'direction(down)',
            'up(1).'       : 'direction(down) direction(right)',
            'up(2).'       : '',
            'up(1).up(2).' : 'direction(down) ',
        }
        for up_states, expected_result in expected_results.items():
            self.assert_running(atoms + up_states, expected_result)

    def test_basic_memory(self):
        self.assert_running(
            'up(1). neuron(1,i). edge(1,2). neuron(2,o). memwrite(2,0).',
            'memory(0)'
        )



class TestNeuronLogicalGates(NeuralNetworkTester):
    """Test all logical gates, with all possible cases of
    predecessor neurons states.

    """
    def setUp(self):
        """Create three input neurons, predecessors of a single neuron and all
        possible cases of input."""
        self.atoms = ('neuron(1,i). neuron(2,i). neuron(3,i).'
                      # neuron 4 will be tested with all possible gates
                      'neuron(4,{}). output(4,left).'
                      'edge(1,4). edge(2,4). edge(3,4).')
        self.cases = {
            # input states     : {expected gates leading to activated direction}
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
                self.assert_running(
                    self.atoms.format(gate[0]) + states,
                    'direction(left)' if gate in expected_result else '',
                )
