"""
Functions designed for convertion of different data, including Individuals
graph into a standard graph format.

"""
import tempfile
from graphviz import Digraph
from collections import defaultdict

from neural_world.atoms import split as atoms_split
from neural_world.commons import NeuronType


def graphdict_to_dot(graph_dict):
    """Return the DOT equivalent to the graph describes in given dict"""
    graph = Digraph()
    for pred, nexts in graph_dict.items():
        pred = str(pred)
        graph.node(pred)
        for succ in (str(_) for _ in nexts):
            graph.node(succ)
            graph.edge(pred, succ)
    return graph.source

def network_atoms_to_dot(network_atoms):
    """Return the DOT formatted string equivalent of given neural network"""
    return network_atoms_to_graphviz(network_atoms).source


def network_atoms_rendering(network_atoms):
    """Print the given network_atoms in pdf. Spam your working screen."""
    return network_atoms_to_graphviz(network_atoms).render(view=True)


def network_atoms_to_graphviz(network_atoms):
    """Create a graphviz.Digraph object from the given network_atoms."""
    atoms = (atoms_split(a) for a in network_atoms.split('.') if a != '')
    graph = defaultdict(str)  # ID: type
    edges = []  # list of 2-tuple

    for name, args in atoms:
        if name == 'output' and len(args) == 1:  # output/1
            idn, = args
            # If already in graph, then idn is an output
            # node already set as neuron.
            graph[idn] += '\n(output)'
        elif name == 'neuron' and len(args) == 2:  # neuron/2
            idn, ntype = args
            graph[idn] = NeuronType(ntype).name + graph.get(idn, '')
        elif name == 'edge' and len(args) == 2:  # edge/2
            ida, idb = args
            edges.append((ida, idb))
        else:
            # some received atoms are not handled…
            # see logs for details
            LOGGER.error('UNHANDLED ATOMS: ' + str((name, args)) + '.')

    # Create and return the dot from graph and edges
    dot = Digraph()
    [dot.node(idn, str(idn) + '\n' + label) for idn, label in graph.items()]
    [dot.edge(a, b) for a, b in edges]
    return dot
