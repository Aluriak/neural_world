import unittest
from pyasp.asp import TermSet

from neural_world.neural_network import (FILE_ASP_CLEANING, FILE_ASP_RUNNING,
                                         NeuralNetwork)
from neural_world.solving import model_from


def comparable_atoms(atoms:str) -> set:
    """Return the same atoms, as comparable data"""
    # make atoms iterable over each atom
    # if atoms is a TermSet or a tuple, it is already done
    if isinstance(atoms, str):
        if ' ' in atoms:
            atoms = atoms.split(' ')
        else:
            atoms = atoms.split('.')
    # return atoms as a set
    return frozenset(atom.strip('.  \n\t') for atom in atoms if len(atom))


class NeuralNetworkTester(unittest.TestCase):
    """Mother class of all ASP solving related unittest.TestCase classes.

    Defines the assert_solving function, designed as high level ASP output test.

    """

    def __assert_solving(self, atoms, expected_result, solve_func):
        solved = comparable_atoms(solve_func(atoms))
        expected = comparable_atoms(expected_result)
        # debug printings
        # print('\n\tATOMS   : ' + str(atoms),
              # '\n\tFOUND   : ' + str(solved),
              # '\n\tEXPECTED: ' + str(expected),
              # '\n\tEQUALITY: ' + str(expected == solved))
        self.assertEqual(solved, expected)

    def assert_cleaning(self, atoms, expected_result):
        """Compare given atoms after cleaning and expected_result,
        using self.assertEqual.

        atoms -- TermSet or iterable of string or string of atoms sep. by space.
        expected_result -- string of atoms separated by space.

        """
        return self.__assert_solving(atoms, expected_result, self._clean)

    def assert_running(self, atoms, expected_result):
        """Compare given atoms after network running and expected_result,
        using self.assertEqual.

        atoms -- TermSet or iterable of string or string of atoms sep. by space.
        expected_result -- string of atoms separated by space.

        """
        return self.__assert_solving(atoms, expected_result, self._run)

    def _clean(self, atoms):
        return model_from(atoms, FILE_ASP_CLEANING)

    def _run(self, atoms):
        return model_from(atoms, FILE_ASP_RUNNING)
