"""
The Archivist is an observer of world.
It saves data like DOT versions of neuron networks,
and keep alive a register of events easily parsable.

"""
import os

import neural_world.config as config
import neural_world.commons as commons
import neural_world.converter as converter
from neural_world.nutrient import Nutrient
from neural_world.individual import Individual
from . import observer


class Archivist(observer.Observer):

    def __init__(self, archive_directory, simulation_id=None):
        # use simulation_id as the name of the subdir in archive directory
        self.simulation_id = str(simulation_id) if simulation_id else ''
        self.archive_directory = os.path.join(archive_directory, self.simulation_id)
        try:
            os.mkdir(self.archive_directory)
        except FileExistsError:
            pass
        # keep the main archive file open, until instance destruction.
        # this file is used by the write(2) method.
        self.archive_file = open(
            os.path.join(self.archive_directory, 'archive.txt'),
            'w'  # erase unexpected existant file
        )

    def __del__(self):
        self.archive_file.close()

    def update(self, world, signals):
        if observer.Signal.NEW_INDIVIDUAL in signals:
            new_indiv, parent = signals[observer.Signal.NEW_INDIVIDUAL]
            # get the cleaned and not cleaned versions of the network
            dot_cln = converter.network_atoms_to_dot(new_indiv.network_atoms)
            dot_all = converter.network_atoms_to_dot(new_indiv.network_atoms_all)
            self.save(new_indiv, dot_cln, 'dot_cln', ext='dot')
            self.save(new_indiv, dot_all, 'dot_all', ext='dot')

    def save(self, indiv, data, description='data', ext='txt'):
        "Save given data for given indiv in its single file"
        # template file is named after self ID, individual ID and save data
        template = os.path.join(self.archive_directory, 'archive_%s_%s.%s')

        filename = template % (indiv.ID, description, ext)
        with open(filename, 'w') as fd:
            fd.write(data)

    def write(self, string):
        "Add given string to the main archive file"
        self.archive_file.write(string)


