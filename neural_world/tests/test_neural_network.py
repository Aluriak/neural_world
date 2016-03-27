"""
Unit tests for neural networks routines.

"""
import unittest

from neural_world import neural_network
from neural_world.tests import NeuralNetworkTester


class TestFunctionsNeuralNetwork(NeuralNetworkTester):

    def setUp(self):
        pass


    def test_simple(self):
        nn = 'neuron(1,i). neuron(2,i). neuron(3,o). output(3). edge(1,3). edge(1,2).'
        self.assert_solving(nn, neural_network.clean(nn))
