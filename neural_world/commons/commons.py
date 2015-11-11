"""
Defines global values, types and access to the logger.

"""
import os
import importlib

from neural_world.info import PACKAGE_NAME


# DIRECTORIES
DIR_PACKAGE  = PACKAGE_NAME + '/'
DIR_LOGS     = DIR_PACKAGE + 'logs/'
DIR_ASP      = DIR_PACKAGE + 'asp/'
DIR_ARCHIVES = DIR_PACKAGE + 'archives/'


def import_classes(dirname, classes_names=None, class_check=lambda x: True):
    """
    Import all modules in directory of given name.
    Given classes_names must be a list of string that contain name of
    wanted classes.
    If given classes_names is None, all founded classes are imported.
    Given class_check is applied on all returned class.
    Return a list of class.
    If a class is not found, a warning will be reported.
    If application of class_check on a class don't return True, a warning will
    be reported.

    """
    # delete void names, and ignore case when no classes are asked
    if classes_names:
        classes_names = [c for c in classes_names if c != '']
        if len(classes_names) == 0: return []
    # initializations
    if classes_names:
        remain_classes = set(c for c in classes_names if c != '')
    found_classes = []
    # open python modules in user classes directory
    # ex: 'evolacc/userclasses/thing.py' -> 'evolacc.userclasses.thing'
    dirname += '' if dirname.endswith('/') else '/'
    modules = (dirname.replace('/', '.')+os.path.splitext(f)[0]
               for f in os.listdir(dirname)
               if os.path.splitext(f)[1] == '.py' and f != '__init__.py'
              )

    # collect all expected classes in userclasses list
    for module in modules:
        # import user module
        module = importlib.import_module(module, package=PACKAGE_NAME)

        # generator over module classes
        classes = (
            module.__getattribute__(attr_name)
            for attr_name in module.__dict__.keys()
            if not attr_name.startswith('_')  # avoid private components
        )
        # get only classes
        classes = (
            attr
            for attr in classes
            if callable(attr) and type(attr) is type
        )
        # filter out classes that are not expected, if classes names are given
        if classes_names:
            classes = (
                cls
                for cls in classes
                if cls in classes_names and class_check(cls)
            )

        # founded classes are not hunted anymore, and will be imported
        for cls in classes:
            found_classes.append(cls)
            if classes_names:
                remain_classes.remove(cls)

    if classes_names and len(remain_classes) > 0:
        LOGGER.warning("__import_user_classes(): classes not found: "
              + ','.join((str(g) for g in remain_classes))
        )

    return found_classes
