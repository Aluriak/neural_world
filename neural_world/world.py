"""
World define space and objects contained in.
It provides an API used by the Actions subclasses.

"""
import itertools
import random
from collections import defaultdict

import neural_world.default as default
import neural_world.commons as commons
import neural_world.observer as observer
from neural_world.space import Space
from neural_world.commons import Configurable
from neural_world.nutrient import Nutrient
from neural_world.individual import Individual


LOGGER = commons.logger('life')


class World(observer.Observable, Configurable):
    """Data container about the simulation.

    Provides API for Actions subclasses and Observers.

    """

    def __init__(self, config):
        observer.Observable.__init__(self)
        Configurable.__init__(self, config=config, config_fields=[
            'space_width', 'space_height',
            'nutrient_regen', 'nutrient_energy', 'nutrient_density',
            'init_indiv_density', 'init_indiv_count', 'neighbor_access',
            'incubator', 'terminated'
        ])

        self.space          = Space((self.space_width, self.space_height))
        self.object_counter = defaultdict(int)
        self.step_number    = 0  # step counter ; just an information

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
            if random.random() < self.nutrient_density:
                square.add(Nutrient())
                self.object_counter[Nutrient] += 1
            if self.init_indiv_density > 0.:
                if random.random() < self.init_indiv_density:
                    self.spawn(square)
        # Add indiv_count individuals in the world, randomly
        if self.init_indiv_count > 0:
            for _ in range(self.init_indiv_count):
                self.spawn(self.random_coords())
        # all observers can begin to work
        self.notify_observers()


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

    def move(self, obj, coords, directions):
        """Move given obj placed at given coords in the given direction"""
        new_coords = commons.Direction.final_coords(coords, directions)
        if not self.space.occuped_at(new_coords):
            self.remove(obj, coords)
            self.add(obj, new_coords)
            coords = new_coords
            LOGGER.debug('MOVE: ' + str(obj) + ': ' + str(coords) + ' -> '
                         + str(directions) + ' -> ' + str(new_coords))

    def pick_nutrient(self, individual, coords):
        """Give to individual the energy of a nutrient at given coords"""
        assert individual.is_individual
        individual.energy += self.consume_nutrient(coords)
        LOGGER.debug('CONSUME NUTRIENTS: ' + str(individual))

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
        self.notify_observers({observer.Signal.NEW_INDIVIDUAL: (new, None, place)})

    def spawn_from(self, indiv, coords):
        """Create and place a new indiv, created from given one at given coords."""
        new = self.incubator.clone(indiv)
        new_coords = self.random_neighbor(coords)
        if not self.space.occuped_at(new_coords):
            self.add(new, new_coords)
            LOGGER.info('REPLICATE: ' + str(indiv) + ' gives ' + str(new) +
                        ' at coords ' + str(new_coords) + '.')
            self.notify_observers({observer.Signal.NEW_INDIVIDUAL:
                                   (new, indiv, new_coords)})

    def random_neighbor(self, coords):
        """Return a random coord, choosen in the neighbors of given coords"""
        return random.choice(tuple(self.neighbor_access(coords)))

    def regenerate_nutrient(self):
        """Place randomly nutrient in the world"""
        for square in self.squares:
            if random.random() <= self.nutrient_regen:
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
        return (random.randrange(self.space_width),
                random.randrange(self.space_height))

    @property
    def have_life(self):
        return self.object_counter[Individual] > 0

    @property
    def ordered_objects(self):
        return (
            (coords, self.space[coords])
            for coords in itertools.product(
                range(self.space_width), range(self.space_height)
            )
        )

    @property
    def squares(self):
        return self.space.values()

    def neighbors(self, coords):
        "Return a generator of coords that are the neighbors of given ones"
        return (
            self.space[neighbor]
            for neighbor in default.NEIGHBOR_ACCESS(coords)
        )

    def deinit(self):
        self.deinit_observers()
