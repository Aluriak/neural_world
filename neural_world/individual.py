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
    """Unit of life, having a neural network and able to move in space."""
    next_individual_id = 1  # useful for give to each instance a unique id

    def __init__(self, neural_network:str, energy:int):
        # Attribution of an unique ID
        self.unique_id = Individual.next_individual_id
        Individual.next_individual_id += 1
        # Life support
        self.neural_network = neural_network
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
        else:  # energy is lower than zero
            engine.add(action.RemoveAction(self, coords))


    def reaction_to(self, neighbors):
        """Return a tuple of Direction instances,
        according to the neighbors situation"""
        states = chain.from_iterable(
            neural_network.square_to_input_neurons(square)
            for square in neighbors
        )
        return self.neural_network.react(states)


    def clone(self, mutator=None, energy:int=None):
        """Return a new Individuals, created with the same data,
        modified by the mutator if provided.

        If energy is None, half of the energy of self will be given
        to the returned clone.

        """
        # life support
        if energy is None:  # split energy between the two individuals
            energy = self.energy // 2
            self.energy = int(self.energy / 2 + 0.5)
        # Create
        return Individual(
            self.neural_network.clone(mutator),
            energy=energy,
        )


    @property
    def memory_size(self):
        return self.neural_network.memory_size

    @property
    def network_atoms(self):
        return self.neural_network.neural_network

    @property
    def network_atoms_all(self):
        return self.neural_network.neural_network_all


    @property
    def is_nutrient(self): return False
    @property
    def is_individual(self): return True

    @property
    def max_neuron_id(self):
        return self.neural_network.nb_neuron

    def __str__(self):
        return str(self.unique_id)
