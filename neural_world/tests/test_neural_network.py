"""
Unit tests for neural networks routines.

"""
import unittest

from neural_world.neural_network import NeuralNetwork
from neural_world.tests import NeuralNetworkTester


class TestCleaningNeuralNetwork(NeuralNetworkTester):

    def test_no_atoms(self):
        nn = ''
        self.assert_cleaning(nn, NeuralNetwork.cleaned(nn))
        self.assert_cleaning(nn, '')

    def test_simple_clean(self):
        nn = 'neuron(1,i). neuron(2,i). neuron(3,o). output(3). edge(1,3). edge(1,2).'
        self.assert_cleaning(nn, NeuralNetwork.cleaned(nn))
        self.assert_cleaning(nn, 'neuron(1,i) neuron(3,o) edge(1,3) output(3)')

    def test_nothing_to_clean(self):
        nn = 'neuron(1,i). neuron(2,o). edge(1,2). output(2).'
        self.assert_cleaning(nn, NeuralNetwork.cleaned(nn))
        self.assert_cleaning(nn, 'neuron(1,i) neuron(2,o) edge(1,2) output(2)')

