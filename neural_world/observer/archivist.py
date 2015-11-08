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
    FILE_TEMPLATE = 'archive_%s_%s.%s'
    FILE_ARCHIVES = 'archive.txt'

    def __init__(self, archive_directory, simulation_id=None):
        # use simulation_id as the name of the subdir in archive directory
        self.simulation_id = 'sim_' + str(simulation_id) if simulation_id else ''
        self.archive_directory = os.path.join(archive_directory, self.simulation_id)
        # create the template file name used for storing data.
        #  template file is named after self ID, individual ID and save data.
        self.template = os.path.join(self.archive_directory,
                                     Archivist.FILE_TEMPLATE)
        # create the directory containing all stored data
        try:
            os.mkdir(self.archive_directory)
        except FileExistsError:
            pass
        # keep the main archive file open, until instance destruction.
        # this file is used by the write(2) method.
        self.archive_file = open(
            os.path.join(self.archive_directory, Archivist.FILE_ARCHIVES),
            'w'  # erase unexpected existant file
        )

    def __del__(self):
        "Close main archive file"
        self.archive_file.close()

    def update(self, world, signals):
        """Intercept new individuals creation for create a snapshot
        of their neural networks, in DOT format and PNG picture."""
        if observer.Signal.NEW_INDIVIDUAL in signals:
            new_indiv, parent = signals[observer.Signal.NEW_INDIVIDUAL]
            network_versions = (
                ('dot_cln', new_indiv.network_atoms),
                ('dot_all', new_indiv.network_atoms_all)
            )
            for version, network_atoms in network_versions:
                graph       = converter.network_atoms_to_dot(network_atoms)
                render_file = self._archive_filename(new_indiv, version, 'png')
                dot_file    = self._archive_filename(new_indiv, version, 'dot')
                converter.graph_rendering(graph, render_file)
                self.save(network_atoms, dot_file)

    def save(self, data, archive_filename):
        "Save given data in file named archive_filename"
        with open(archive_filename, 'w') as fd:
            fd.write(data)

    def write(self, string):
        "Add given string to the main archive file"
        self.archive_file.write(string)

    def _archive_filename(self, indiv, description='data', ext='txt'):
        "Return file name for given parameters"
        return self.template % (indiv.ID, description, ext)
