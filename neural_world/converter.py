"""
Functions designed for convertion of different data, including Individuals
graph into a standard graph format.

"""
import tempfile
from enum import Enum
from collections import defaultdict

import pygraphviz as pgv

from neural_world.atoms import split as atoms_split
from neural_world import commons
from neural_world.commons import NeuronType


LOGGER = commons.logger()


class GraphvizLayout(Enum):
    """Graphiz layouts for graph rendering that are usable
    from scratch with pygraphviz module"""
    neato   = 'neato'
    dot     = 'dot'
    twopi   = 'twopi'
    circo   = 'circo'
    fdp     = 'fdp'
    sfdp    = 'sfdp'


def graphdict_to_dot(graph_dict):
    """Return the DOT equivalent to the graph describes in given dict"""
    graph = pgv.AGraph(strict=False, directed=True)
    for pred, nexts in graph_dict.items():
        # pred = str(pred)
        graph.add_node(pred)
        # for succ in (str(_) for _ in nexts):
        for succ in (_ for _ in nexts):
            graph.add_node(succ)
            graph.add_edge(pred, succ)
    return str(graph)


def network_atoms_to_dot(network_atoms):
    """Return the DOT formatted string equivalent of given neural network"""
    return str(network_atoms_to_graphviz(network_atoms))


def graph_rendering(graph_data, filename='output.png', layout=GraphvizLayout.dot):
    """Draw the given graph in given filename.

    graph_data: DOT formatted string describing a graph
        (return value of  network_atoms_to_dot(1)),
        or a pygraphviz.AGraph instance.
    filename: file where the rendering will be saved.
    layout: program used by graphviz for drawing the graph.
        (see GraphvizLayout for available values)
    return: the pygraphviz.AGraph instance that have been rendered.

    """
    # convert network_atoms in pgv.AGraph, if necessary
    if isinstance(graph_data, pgv.AGraph):
        graph = graph_data
    else:  # graph_data is a dot formatted string
        graph = pgv.AGraph(graph_data)  # create an AGraph directly from dot
    graph.draw(filename, prog=layout.value)
    return graph


def network_atoms_to_graphviz(network_atoms):
    """Create a pygraphviz.AGraph object from the given network_atoms."""
    atoms = (atoms_split(a) for a in network_atoms.split('.') if a != '')
    graph = defaultdict(str)  # ID: type
    edges = []  # list of 2-tuple

    for name, args in atoms:
        if name == 'output' and len(args) == 1:  # output/1
            # If already in graph, then idn is an output
            # node already set as neuron.
            graph[args] += '\n(output)'
        elif name == 'neuron' and len(args) == 2:  # neuron/2
            idn, ntype = args
            graph[idn] = NeuronType(ntype).name + graph.get(idn, '')
        elif name == 'edge' and len(args) == 2:  # edge/2
            ida, idb = args
            edges.append((ida, idb))
        else:
            # some received atoms are not handled…
            # see logs for details
            LOGGER.error('converter.network_atoms_to_graphviz:'
                         ' UNHANDLED ATOMS: ' + str((name, args)) + '.')

    # Create and return the dot from graph and edges
    dot = pgv.AGraph(strict=False, directed=True)
    [dot.add_node(idn, label=str(idn) + '\n' + label) for idn, label in graph.items()]
    [dot.add_edge(a, b) for a, b in edges]
    return dot
