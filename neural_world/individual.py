"""
Individual is a class that keep together id, dna and neural networks.

"""
from itertools import islice, chain

import neural_world.actions as action
import neural_world.default as default
import neural_world.commons as commons
from neural_world.commons import Direction
from neural_world import neural_network


LOGGER = commons.logger('life')


class Individual:
    """
    """
    next_individual_id = 1  # useful for give to each instance a unique id

    def __init__(self, nb_intermediate_neuron, neuron_types, edges, energy):
        # Attribution of an unique ID
        self.unique_id = Individual.next_individual_id
        Individual.next_individual_id += 1
        # Management of neural network data
        self.nb_intermediate_neuron = nb_intermediate_neuron
        self.nb_neuron = Individual.neuron_total_count(nb_intermediate_neuron)
        self.neuron_types = tuple(neuron_types)
        self.edges = tuple(edges)
        # Construction of the neural network
        self.network_atoms_all = Individual.build_network_atoms(self)
        assert self.network_atoms_all.count('neuron') == self.nb_neuron
        # Cleaning, for remove useless data
        self.network_atoms = neural_network.clean(self.network_atoms_all)
        assert self.network_atoms[-1] == '.'
        # Life support
        self.energy = energy

    def update(self, engine, neighbors, coords):
        """Compute the next step and send command to the given engine"""
        # Life cost
        self.energy -= 1
        # Pick Nutrient
        engine.add(action.PickNutrientAction(self, coords))
        # Life support: replicate, move or die
        if self.energy >= default.LIFE_DIVISION_MIN_ENERGY:
            engine.add(action.ReplicateAction(self, coords))
        elif self.energy > 0:
            # get states of input neurons and react to it
            directions = self.reaction_to(neighbors)
            engine.add(action.MoveAction(self, coords, directions))
        else:
            engine.add(action.RemoveAction(self, coords))


    def reaction_to(self, neighbors):
        """Return a tuple of Direction instances,
        according to the neighbors situation"""
        states = chain.from_iterable(
            neural_network.square_to_input_neurons(square)
            for square in neighbors
        )
        return neural_network.react(self, states)


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
        # apply the mutator if available, and create the Individual
        if mutator:
            nb_intermediate_neuron, neuron_types, edges = mutator.mutate(
                nb_intermediate_neuron, neuron_types, edges
            )
        return Individual(
            nb_intermediate_neuron=nb_intermediate_neuron,
            neuron_types=neuron_types,
            edges=edges,
            energy=energy,
        )


    @staticmethod
    def build_network_atoms(individual):
        "Build and save the atoms describing the neural network."
        # generator of ids. It must be a generator, for provides only one time
        #  each neuron in multiple partial reads.
        neuron_ids = (_ for _ in range(1, individual.nb_neuron + 1))
        return '.'.join(chain(
            # input neurons
            ('neuron(' + str(idn) + ','
             + default.INPUT_NEURON_TYPE.value + ')'
             for idn in islice(neuron_ids, 0, default.INPUT_NEURON_COUNT)),
            # intermediate neurons
            ('neuron(' + str(idn) + ',' + neuron_type.value + ')'
             for idn, neuron_type in zip(
                 islice(neuron_ids, 0, individual.nb_intermediate_neuron),
                 individual.neuron_types
             )),
            # # output neurons: give their type and their output status.
            ('neuron(' + str(idn) + ',' + default.OUTPUT_NEURON_TYPE.value
             + ').output(' + str(idn) + ')'  # this neuron is an output
             for idn in neuron_ids),  # all remaining IDs are for output neurons
            # edges
            ('edge(' + str(id1) + ',' + str(id2) + ')'
             for id1, id2 in individual.edges)
        )) + '.'

    @staticmethod
    def neuron_total_count(nb_intermediate_neuron):
        """Return the total number of neuron present in an individual
        with given number of intermediate neuron."""
        return sum((
            default.INPUT_NEURON_COUNT, default.OUTPUT_NEURON_COUNT,
            nb_intermediate_neuron
        ))

    @property
    def is_nutrient(self): return False
    @property
    def is_individual(self): return True

    @property
    def max_neuron_id(self): return self.nb_neuron

    def __str__(self):
        return str(self.unique_id) + ': I-Neurons: ' + str(self.nb_intermediate_neuron)
