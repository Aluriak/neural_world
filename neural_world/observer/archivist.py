"""
The Archivist is an observer of world.
It saves data like DOT versions of neuron networks,
and keep alive a register of events easily parsable.

"""
import os
from functools import partial

import neural_world.commons as commons
import neural_world.actions as action
import neural_world.converter as converter
from neural_world.nutrient import Nutrient
from neural_world.individual import Individual
from . import observer


class Archivist(observer.Observer, action.ActionEmitter):
    FILE_TEMPLATE = 'archive_%s_%s.%s'
    FILE_ARCHIVES = 'archive.txt'
    GRAPHVIZ_LAYOUT = converter.GraphvizLayout.dot

    def __init__(self, engine, archive_directory, simulation_id=None, *,
                 save_graph=True, render_graph=True):
        super().__init__(invoker=engine)
        # data saving options
        self.save_graph = save_graph
        self.render_graph = render_graph
        self.do_graph = any((save_graph, render_graph))
        # use simulation_id as the name of the subdir in archive directory
        self.simulation_id = 'sim_' + str(simulation_id) if simulation_id else ''
        self.archive_directory = archive_directory
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
        if self.do_graph and observer.Signal.NEW_INDIVIDUAL in signals:
            new_indiv, parent = signals[observer.Signal.NEW_INDIVIDUAL]
            gen_filename = partial(self._archive_filename, new_indiv)
            network_versions = (
                ('dot_cln', new_indiv.network_atoms),
                ('dot_all', new_indiv.network_atoms_all)
            )
            for version, network_atoms in network_versions:
                graph = converter.network_atoms_to_dot(network_atoms)
                if self.save_graph:
                    dot_file = gen_filename(version, 'dot')
                    self.save(graph, dot_file)
                if self.render_graph:
                    render_file = gen_filename(version, 'png')
                    converter.graph_rendering(graph, render_file,
                                              layout=Archivist.GRAPHVIZ_LAYOUT)

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

    @staticmethod
    def archive_directory(archive_directory='', simulation_id=''):
        return os.path.join(archive_directory, simulation_id)
