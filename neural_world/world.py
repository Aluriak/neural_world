"""
World define space and objects contained in.
It provides an API used by the Actions subclasses.

"""
import itertools
from random import random, randrange
from collections import defaultdict

import neural_world.config as config
import neural_world.commons as commons
import neural_world.observer as observer
from neural_world.nutrient import Nutrient
from neural_world.individual import Individual
from neural_world.bounded_defaultdict import BoundedDefaultDict


LOGGER = commons.logger('life')


class World(observer.Observable):
    """Data container about the simulation.

    Provides API for Actions subclasses and Observers.

    """

    def __init__(self, width:int, height:int, incubator,
                 nutrient_density:float, nutrient_regen:float,
                 indiv_density:float=None, indiv_count:int=None):
        super().__init__()
        self.width, self.height = width, height
        self.space              = BoundedDefaultDict((width, height), set)
        self.incubator          = incubator
        self.nutrient_density   = nutrient_density
        self.nutrient_regen     = nutrient_regen
        self.indiv_density      = indiv_density
        self.indiv_count        = indiv_count
        self.object_counter     = defaultdict(int)
        self.step_number        = 0
        self.finished           = False  # just an indication flag

    def populate(self):
        """Populate the world as in initial case.

        Note that without call this before any other treatment,
        some methods can go wrong and the space can be
        totally uninintialized.
        Call this after register all observers seems to be a good idea, as some
        initialization treatment (first individuals spawning for example) can
        interest some of them.

        """
        # Populate the world according to densities
        for coords, square in self.ordered_objects:
            if random() < self.nutrient_density:
                square.add(Nutrient())
                self.object_counter[Nutrient] += 1
            if self.indiv_density and random() < self.indiv_density:
                self.spawn(square)
        # Add indiv_count individuals in the world, randomly
        if self.indiv_count:
            for _ in range(self.indiv_count):
                self.spawn(self.random_coords())


    def remove(self, obj, place):
        """Remove an object from space at given coords/square, and return it.

        obj: an individual or a nutrient.
        place: coords (2-tuple) or square (set) from obj will be removed.

        """
        if isinstance(place, set): square = place
        else:                      square = self.space[place]
        square.remove(obj)
        self.object_counter[obj.__class__] -= 1
        return obj

    def add(self, obj, place):
        """Place given obj at given coords or square, and return it.

        obj: an individual or a nutrient.
        place: coords (2-tuple) or square (set) where the obj will be placed.

        """
        if isinstance(place, set):  # its a square !
            place.add(obj)
        else:  # its coords !
            self.space[place].add(obj)
        self.object_counter[obj.__class__] += 1
        return obj

    def spawn(self, place=None):
        """Create and place a new indiv, created from incubator."""
        # Use random coords if no coords given
        if place is None:
            place = self.random_coords()
        # Create the new indiv and add it to space
        new = self.incubator.spawn()
        self.add(new, place)
        # Logs it and send signal to observers
        LOGGER.info('NEW INDIVIDUAL: ' + str(new) + '.')
        self.notify_observers({observer.Signal.NEW_INDIVIDUAL: (new, None)})

    def spawn_from(self, indiv, coords):
        """Create and place a new indiv, created from given one."""
        new = self.incubator.clone(indiv)
        self.add(new, coords)
        LOGGER.info('REPLICATE: ' + str(indiv) + ' gives ' + str(new) + '.')
        self.notify_observers({observer.Signal.NEW_INDIVIDUAL: (new, indiv)})

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

    def deinit(self):
        self.deinit_observers()
