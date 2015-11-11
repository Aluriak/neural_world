"""
This submodule contains all Observer implementations, as the Observer,
Observable and signal classes/enum.

"""
from os.path import dirname, relpath

from neural_world.commons import import_classes
from neural_world.observer.observer  import Signal, Observable, Observer


# import all classes for all modules of observer submodule
for cls in import_classes(relpath(dirname(__file__))):
    globals()[cls.__name__] = cls
