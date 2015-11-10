"""
Definition of the Direction enumeration.

"""
import itertools

from enum import IntEnum
from functools import reduce
from collections import Counter


class Direction(IntEnum):
    """Enumeration of the four possible movement directions.

    This class provides a rich API for manipulate and play with directions.

    """
    up, right, down, left = 0, 1, 2, 3

    @property
    def opposite(self):
        "Return the opposite of self"
        return Direction((self + 2) % 4)

    def is_opposite(self, othr) -> bool:
        "True if self and other are opposites"
        return self.opposite is othr

    @staticmethod
    def neighbor(coords, direction):
        "Return the neighbor coordinates of given coords, in given direction"
        x, y = coords
        if   direction is Direction.up:    return x    , y - 1
        elif direction is Direction.right: return x + 1, y
        elif direction is Direction.down:  return x    , y + 1
        elif direction is Direction.left:  return x - 1, y

    @staticmethod
    def final_coords(coords, directions):
        "Coords reached after moves in given directions from given coords"
        return tuple(reduce(Direction.neighbor,
                     itertools.chain([coords], directions)))

    @staticmethod
    def simplified(directions):
        "Return an iterable of directions, that is in absolute equivalent to the given one"
        c = Counter(directions)
        sum_up = c[Direction.up] - c[Direction.down]
        dir_up = Direction.up if sum_up > 0 else Direction.down
        sum_left = c[Direction.left] - c[Direction.right]
        dir_left = Direction.left if sum_left > 0 else Direction.right
        return itertools.chain(
            itertools.repeat(dir_up, times=abs(sum_up)),
            itertools.repeat(dir_left, times=abs(sum_left)),
        )

    def __str__(self):
        return self.name

assert     Direction.up.is_opposite(Direction.down)
assert     Direction.left.is_opposite(Direction.right)
assert not Direction.up.is_opposite(Direction.right)
assert     Direction.left.opposite is Direction.right
assert     Direction.down.opposite is Direction.up
assert not Direction.left.opposite is Direction.up



