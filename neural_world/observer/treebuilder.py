"""
Observer of World that maintain a tree of life.

"""
import os
from collections import defaultdict

import neural_world.converter as converter
from . import observer


class TreeBuilder(observer.Observer):
    """Observer of World that maintain a tree of life"""

    def __init__(self, archive_directory):
        self.tree = defaultdict(list)
        self.archive_directory = archive_directory

    def update(self, world, signals):
        if observer.Signal.NEW_INDIVIDUAL in signals:
            new, parent = signals[observer.Signal.NEW_INDIVIDUAL]
            if parent:
                self.tree[parent.ID].append(new.ID)

    def postprocessing(self, world):
        """Save the tree in file"""
        with open(os.path.join(self.archive_directory, 'tree'), 'w') as fd:
            fd.write(converter.graphdict_to_dot(self.tree))
