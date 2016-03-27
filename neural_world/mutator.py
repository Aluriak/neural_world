"""
Mutators are objects capable of modify data exploited by Individuals, allowing
 mutation of the population.

"""
import logging
from random import random, randrange, choice as random_choice

import neural_world.default as default
import neural_world.commons as commons
from neural_world.commons import Direction
from neural_world.commons import NeuronType
from neural_world.individual import Individual
from neural_world.commons import Configurable
from neural_world.neural_network import NeuralNetwork


LOGGER = commons.logger('life')


class Mutator(Configurable):

    def __init__(self, config):
        super().__init__(config, config_fields=[
            'mutation_rate',
        ])

    def mutate(self, nb_intermediate_neuron:int, nb_total_neuron:int,
               neuron_types:iter, edges:iter):
        """Return the data received in input, modified according to
        mutation settings.

        nb_intermediate_neuron: integer equal to number of intermediate neuron.
        nb_total_neuron: integer equal to total number of neuron.
        neuron_types: iterable of NeuronType.
        edges: iterable of 2-tuple describing links between neurons.

        """
        MUTATION_RATE = self.mutation_rate
        mutate_nb_neuron   = random() <= MUTATION_RATE, random() <= MUTATION_RATE
        mutate_neuron_type = random() <= MUTATION_RATE, random() <= MUTATION_RATE
        mutate_edges       = random() <= MUTATION_RATE, random() <= MUTATION_RATE

        if any(mutate_nb_neuron):
            add, rmv = mutate_nb_neuron
            neuron_types = list(neuron_types)  # allow modifications
            if add:
                nb_intermediate_neuron += 1
                neuron_types.append(random_choice(NeuronType.xano()))
                if commons.log_level() >= logging.INFO:
                    LOGGER.info('Mutator ' + str(self)
                                 + ' add new neuron of type '
                                 + neuron_types[-1].name + '.')
            if rmv:  # delete one intermediate neuron
                nb_intermediate_neuron -= 1
                target_idx = randrange(0, len(neuron_types))
                if commons.log_level() >= logging.INFO:
                    LOGGER.info('Mutator ' + str(self)
                                 + ' remove neuron ' + str(target_idx) + ' ('
                                 + neuron_types[target_idx].name + ').')
                del neuron_types[target_idx]

        if any(mutate_neuron_type):
            modify, swap = mutate_neuron_type
            neuron_types = list(neuron_types)  # allow modifications
            if modify:  # modify just one type
                target_idx = randrange(0, len(neuron_types))
                new_type = random_choice(NeuronType.xano())
                if commons.log_level() >= logging.INFO:
                    LOGGER.info('Mutator ' + str(self) + ' modify type of '
                                 + str(target_idx) + ' from '
                                 + neuron_types[target_idx].name + ' to '
                                 + new_type.name + '.'
                                )
                neuron_types[target_idx] = new_type
            if swap:  # swap two types in the list
                target1_idx = randrange(0, len(neuron_types))
                target2_idx = randrange(0, len(neuron_types))
                neuron_types[target1_idx], neuron_types[target2_idx] = (
                    neuron_types[target2_idx], neuron_types[target1_idx]
                )
                if commons.log_level() >= logging.INFO:
                    LOGGER.info('Mutator ' + str(self) + ' swaps '
                                 + str(target1_idx) + ' ('
                                 + neuron_types[target2_idx].name + ') and '
                                 + str(target1_idx) + ' ('
                                 + neuron_types[target2_idx].name + ').'
                                )
        if any(mutate_edges):
            add, rmv = mutate_edges
            edges = list(edges)  # allow modifications
            if add:  # add one new edge
                target1_idx = randrange(1, nb_total_neuron + 1)
                target2_idx = randrange(1, nb_total_neuron + 1)
                edges.append((target1_idx, target2_idx))
                if commons.log_level() >= logging.INFO:
                    LOGGER.info('Mutator ' + str(self) + ' get an edge '
                                 + str((target1_idx, target2_idx)) + '.')
            if rmv:  # remove one existing edge
                idx = randrange(0, len(edges))
                if commons.log_level() >= logging.INFO:
                    LOGGER.info('Mutator ' + str(self) + ' lose its edge '
                                 + str(edges[idx]) + '.')

        return (nb_intermediate_neuron, nb_total_neuron,
                tuple(neuron_types), tuple(edges))
