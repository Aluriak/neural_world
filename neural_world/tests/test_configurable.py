"""
Unit tests for Configurable class.

"""
import unittest

from neural_world.commons import Configurable


class TestClassConfigurable(unittest.TestCase):

    def setUp(self):
        class ConfigMock:
            def __init__(self, a=42):
                self.a = a
                self.b = 'hello, world'
                self.c = False
        self.config = ConfigMock()
        self.new_config = ConfigMock(a='is propagation working ?')
        self.m1 = Configurable(self.config, config_fields=['a', 'b'])
        self.m2 = Configurable(self.config, config_fields=['b', 'c'])
        self.m2.other_m = self.m1  # m2 know m1


    def test_init(self):
        self.assertEqual(self.config.b, self.m2.b)
        self.assertEqual(self.config.a, self.m1.a)
        self.config.b == self.m1.b
        self.assertFalse(hasattr(self.m1, 'c'))

    def test_sharing(self):
        self.assertFalse(hasattr(self.m2, 'a'))
        self.assertEqual(self.config.b, self.m2.b)
        self.assertEqual(self.config.c, self.m2.c)

    def test_propagation(self):
        # update config: use new_config where field 'a' have changed
        self.m2.config = self.new_config  # change configuration of m2 (so of m1, too)
        self.assertEqual(self.new_config.a, self.m1.a)  # m1 change for the new config
        self.assertFalse(hasattr(self.m2, 'a'))  # m2 doesn't care about the changed field
