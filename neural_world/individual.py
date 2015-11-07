"""
Individual is a class that keep together id, dna and neural networks.

"""
from itertools import islice, chain

import neural_world.config as config
import neural_world.commons as commons
from neural_world.commons import Direction
from neural_world.commons import NeuronType
from neural_world.actions import MoveAction, RemoveAction
from neural_world import neural_network


class Individual:
    next_individual_id  = 1  # useful for give to each instance a unique id

    def __init__(self, nb_intermediate_neuron, neuron_types, edges, energy):
        # Attribution of an unique ID
        self.ID = Individual.next_individual_id
        Individual.next_individual_id += 1
        # Management of neural network data
        self.nb_intermediate_neuron = nb_intermediate_neuron
        self.nb_neuron = sum((
            config.INPUT_NEURON_COUNT, config.OUTPUT_NEURON_COUNT,
            nb_intermediate_neuron
        ))
        self.neuron_types = tuple(neuron_types)
        self.edges = tuple(edges)
        # Construction of the neural network
        self.network_atoms = Individual.build_network_atoms(self)
        assert self.network_atoms.count('neuron') == self.nb_neuron
        # Cleaning, for remove useless data
        self.network_atoms = neural_network.clean(self.network_atoms)
        # Life support
        self.energy = energy

    def update(self, engine, neighbors, coords):
        """Compute the next step and send command to the given engine"""
        # Life support
        self.energy -= 1
        if self.energy > 0:
            # get states of input neurons and react to it
            states = chain.from_iterable(
                neural_network.square_to_input_neurons(square)
                for square in neighbors
            )
            directions = neural_network.react(self, states)
            engine.add(MoveAction(self, coords, directions))
        else:
            engine.add(RemoveAction(self, coords))


    def clonage(self, mutator=None, energy=None):
        """Return a new Individuals, created with the same data,
        modified by the mutator if provided.

        If energy is None, half of the energy keeped by self will be given
        to the new clone.

        """
        # copy the data
        nb_intermediate_neuron = self.nb_intermediate_neuron
        neuron_types = tuple(self.neuron_types)
        edges = tuple(self.edges)
        if energy is None:
            energy = self.energy // 2
            self.energy = int(self.energy / 2 + 0.5)
        # apply the mutator if available
        if mutator:
            nb_intermediate_neuron, neuron_types, edges = mutator.mutate(
                nb_intermediate_neuron, neuron_types, edges
            )
        return Individual(
            nb_intermediate_neuron=nb_neuron,
            neuron_types=types,
            edges=edges,
            energy=energy,
        )


    @staticmethod
    def build_network_atoms(individual):
        "Build and save the atoms describing the neural network."
        # generator of ids. It must be a generator, for provides only one time
        #  each neuron in multiple partial reads.
        neuron_ids = (_ for _ in range(1, individual.nb_neuron + 1))
        return ''.join(chain(
            # input neurons
            ('neuron(' + str(idn) + ','
             + config.INPUT_NEURON_TYPE.value + ').'
             for idn in islice(neuron_ids, 0, config.INPUT_NEURON_COUNT)),
            # intermediate neurons
            ('neuron(' + str(idn) + ',' + neuron_type.value + ').'
             for idn, neuron_type in zip(
                 islice(neuron_ids, 0, individual.nb_intermediate_neuron),
                 individual.neuron_types
             )),
            # # output neurons: give their type and their output status.
            ('neuron(' + str(idn) + ',' + config.OUTPUT_NEURON_TYPE.value
             + ').output(' + str(idn) + ').'  # this neuron is an output
             for idn in neuron_ids),  # all remaining IDs are for output neurons
            # edges
            ('edge(' + str(id1) + ',' + str(id2) + ').'
             for id1, id2 in individual.edges)
        ))

    @property
    def is_nutrient(self): return False
    @property
    def is_individual(self): return True

    @property
    def max_neuron_id(self): return self.nb_neuron

    def __str__(self):
        return str(self.ID) + ': I-Neurons: ' + str(self.nb_intermediate_neuron)
