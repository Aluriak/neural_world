"""
Observer of World that maintain a tree of life.

"""
import os
from collections import defaultdict

import neural_world.converter as converter
import neural_world.actions as action
from . import observer


class TreeBuilder(observer.Observer, action.ActionEmitter):
    """Observer of World that maintain a tree of life"""
    GRAPHVIZ_LAYOUT = converter.GraphvizLayout.twopi

    def __init__(self, engine, archive_directory, render_graph=True):
        super().__init__(invoker=engine)
        self.tree = defaultdict(list)
        self.archive_directory = archive_directory
        self.render_graph = render_graph

    def update(self, world, signals):
        if observer.Signal.NEW_INDIVIDUAL in signals:
            new, parent = signals[observer.Signal.NEW_INDIVIDUAL]
            if parent:
                self.tree[parent.ID].append(new.ID)

    def postprocessing(self, world):
        """Save the tree in file, and its rendering"""
        filename = os.path.join(self.archive_directory, 'tree')
        dot = converter.graphdict_to_dot(self.tree)
        with open(filename, 'w') as fd:
            fd.write(dot)
        if self.render_graph:
            converter.graph_rendering(dot, filename + '.png',
                                      layout=TreeBuilder.GRAPHVIZ_LAYOUT)
