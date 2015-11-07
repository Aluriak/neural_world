"""
World define space and objects contained in.
It provides an API used by the Actions subclasses.

"""
import itertools
from random import random, randrange
from collections import defaultdict

import neural_world.config as config
import neural_world.commons as commons
from neural_world.nutrient import Nutrient
from neural_world.individual import Individual
from neural_world.bounded_defaultdict import BoundedDefaultDict


LOGGER = commons.logger('life')


class World:
    """Data container about the simulation.

    Provides API for Actions subclasses and Observers.

    """

    def __init__(self, width:int, height:int, incubator,
                 nutrient_density:float, nutrient_regen:float,
                 indiv_density:float):
        self.width, self.height = width, height
        self.space              = BoundedDefaultDict((width, height), set)
        self.incubator          = incubator
        self.nutrient_density   = nutrient_density
        self.nutrient_regen     = nutrient_regen
        self.indiv_density      = indiv_density

        # Populate the world
        for coords, square in self.ordered_objects:
            if random() < nutrient_density:
                square.add(Nutrient())
            if random() < indiv_density:
                square.add(self.incubator.spawn())

        # Others
        self.observers = set()


    def remove(self, obj, coords):
        """Remove an object from space at given coords, and return it"""
        square = self.space[coords]
        square.remove(obj)
        return obj

    def add(self, obj, coords):
        """Place given obj at given coords, and return it"""
        self.space[coords].add(obj)
        return obj

    def spawn_from(self, indiv, coords):
        """Create and place a new indiv, created from given one."""
        new = self.incubator.clone(indiv)
        self.add(new, coords)
        LOGGER.info('REPLICATE: ' + str(indiv) + ' gives ' + str(new) + '.')

    def regenerate_nutrient(self):
        """Place randomly nutrient in the world"""
        for square in self.squares:
            if random() < self.nutrient_regen:
                square.add(Nutrient())

    def consume_nutrient(self, coords):
        """Remove a Nutrient instance from coords and return
        the associated amount of energy."""
        square = self.space[coords]
        nutrient = None
        for obj in square:
            if obj.is_nutrient:
                nutrient = obj
                break
        if nutrient:
            self.remove(nutrient, coords)
            return nutrient.energy
        else:
            return 0

    def __iter__(self):
        return (
            (coords, obj)
            for coords, objects in self.space.items()
            for obj in objects
        )

    def random_coords(self):
        return (randrange(self.width), randrange(self.height))

    @property
    def have_life(self):
        return self.object_counter[Individual] > 0

    @property
    def ordered_objects(self):
        return (
            (coords, self.space[coords])
            for coords in itertools.product(
                range(self.width), range(self.height)
            )
        )

    @property
    def squares(self):
        return self.space.values()

    def neighbors(self, coords):
        "Return a generator of coords that are the neighbors of given ones"
        return (
            self.space[neighbor]
            for neighbor in config.NEIGHBOR_ACCESS(coords)
        )

    def register(self, observer):
        "Add given observer to set of observers"
        self.observers.add(observer)

    def unregister(self, observer):
        "Remove given observer from set of observers"
        self.observers.remove(observer)

    def notify(self, *args, **kwargs):
        "notify all observers"
        [o.update(self, *args, **kwargs) for o in self.observers]
