"""
Definition of the Space class that placement of objects in space.

"""
from collections import defaultdict


class Space(defaultdict):
    """Dictionnary (coords in k-dimension space):(set of object) that handle
    space borders.

    Needs bounds in N^k at construction.

    This assume that all keys are k-tuple of integers in N, and ensure
    that values in keys will never overpass the bound
    in associated dimension.

    """

    def __init__(self, bounds):
        "Bounds must be maximal values reachable by coords"
        super().__init__(set)
        self.bounds = bounds

    def fix_key(self, key):
        "Return the key, modified for being in the bounds"
        return tuple(
            value % bound
            for value, bound in zip(key, self.bounds)
        )

    def __getitem__(self, key):
        return super().__getitem__(self.fix_key(key))

    def occuped_at(self, coords):
        """Return True iff an individual is present at given coords"""
        return any(obj.is_individual for obj in self[coords])
