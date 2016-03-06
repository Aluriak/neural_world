"""
Unit tests for neural networks routines.

"""
import unittest

from neural_world import neural_network


class TestFunctionsNeuralNetwork(unittest.TestCase):

    def setUp(self):
        pass


    def test_simple(self):
        nn = 'neuron(1,i). neuron(2,i). neuron(3,o). edge(1,3). edge(1,2).'
        # TODO
