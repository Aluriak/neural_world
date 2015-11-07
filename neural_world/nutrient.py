"""
Object placed in the World, consummed by Individuals.

"""


class Nutrient:

    def __init__(self, energy=1):
        self.energy = energy

    def update(self, engine, neighbors, coords):
        pass

    @property
    def is_nutrient(self): return True
    @property
    def is_individual(self): return False
