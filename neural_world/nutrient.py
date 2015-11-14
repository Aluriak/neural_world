"""
Object placed in the World, consummed by Individuals.

"""
import neural_world.default as default


class Nutrient:

    def __init__(self, energy=default.NUTRIENT_ENERGY):
        self.energy = energy

    def update(self, engine, neighbors, coords):
        pass

    @property
    def is_nutrient(self): return True
    @property
    def is_individual(self): return False
