"""
Individual is a class that keep together id, dna and neural networks.

"""
from itertools import islice, chain
from collections import defaultdict

import tergraw

from neural_world import actions
from neural_world import default
from neural_world import commons
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
        engine.add(actions.PickNutrientAction(self, coords))
        # Life support
        if self.energy > 0:
            # get states of input neurons and react to it
            for action in self.reaction_to(neighbors, individual=self, coords=coords):
                if action:
                    engine.add(action)
        else:  # energy is lower than zero
            engine.add(actions.RemoveAction(self, coords))


    def reaction_to(self, neighbors, **kwargs):
        """Yield actions instances, according to the neighbors and kwargs"""
        actions = self.neural_network.react(neighbors=neighbors, **kwargs)
        yield from (action for action in actions if action is not None)


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
    def prettyfied_neural_network(self):
        """Yield the lines of a terminal view of neural network"""
        if self.network_dict:
            yield from tergraw.pretty_view(self.network_dict, oriented=True)
        else:
            yield ''  # nothing to print

    @property
    def network_dict(self):
        if not hasattr(self, '_network_dict'):
            graph, neuron, output = defaultdict(set), {}, set()
            for atom in self.network_atoms.split('.'):
                if not atom: continue
                predicate, args = atom.split('(')
                args = args.rstrip(')').split(',')
                if predicate == 'edge':
                    node, succ = args
                    graph[node].add(succ)
                if predicate == 'neuron':
                    idx, type = args
                    neuron[idx] = type
                if predicate == 'output':
                    output.add(args[0])
                if predicate == 'memwrite':
                    idx, regaddr = args
                    output[idx] = regaddr

            # graph enrichment
            node_name = {
                node: (node + ('-' + neuron[node] if neuron.get(node) else '')
                            + ('-out' if node in output else ''))
                for node in chain(graph.keys(), *graph.values())
            }
            self._network_dict = {
                node_name[node]: set(node_name[succ] for succ in succs)
                for node, succs in graph.items()
            }

        return self._network_dict

    @property
    def is_nutrient(self): return False
    @property
    def is_individual(self): return True

    @property
    def max_neuron_id(self):
        return self.neural_network.nb_neuron

    def __str__(self):
        return str(self.unique_id)
