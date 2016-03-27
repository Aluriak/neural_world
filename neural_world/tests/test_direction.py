"""Unit tests about the Direction Enumeration"""

import unittest
from neural_world.commons import Direction

DIRECTIONS_NAMES = ('up', 'left', 'down', 'right')

class TestDirection(unittest.TestCase):

    def test_iter(self):
        self.assertEqual(set(DIRECTIONS_NAMES), set(Direction.names()))

    def test_access(self):
        for dir in DIRECTIONS_NAMES:
            self.assertIn(Direction[dir], Direction)

    def test_opposite_relations(self):
        self.assertTrue(Direction.up.is_opposite(Direction.down))
        self.assertTrue(Direction.left.is_opposite(Direction.right))
        self.assertFalse(Direction.up.is_opposite(Direction.right))
        self.assertIs(Direction.left.opposite, Direction.right)
        self.assertIs(Direction.down.opposite, Direction.up)
        self.assertIsNot(Direction.left.opposite, Direction.up)
