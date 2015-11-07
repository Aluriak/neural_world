"""
Definition of a defaultdict subclass that handles limits in the space.

"""
from collections import defaultdict


class BoundedDefaultDict(defaultdict):
    """Needs bounds in N^k at construction.

    This assume that all keys are k-tuple of integers in N, and ensure
    that values in keys will never overpass the bound
    in associated dimension.

    """

    def __init__(self, bounds, defaultvalue=None):
        "Bounds must be maximal values reachable by values in keys"
        super().__init__(defaultvalue)
        self.bounds = bounds

    def fix_key(self, key):
        "Return the key, modified for being in the bounds"
        return tuple(
            value % bound
            for value, bound in zip(key, self.bounds)
        )

    def __getitem__(self, key):
        return super().__getitem__(self.fix_key(key))
