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



def import_classes(dirname, classes_names, class_check=lambda x: True):
    """
    Import all modules in directory of given name.
    Given classes_names must be a list of string that contain name of
    wanted classes.
    Given class_check is applied on all returned class.
    Return a list of class.
    If a class is found multiple times, it will be added multiple times.
    If a class is not found, a warning will be reported.
    If application of class_check on a class don't return True, a warning will
    be reported.
    """
    # delete void names, and ignore case when no classes are asked
    classes_names = [c for c in classes_names if c != '']
    if len(classes_names) == 0: return []
    # initializations
    remain_classes = set(c for c in classes_names if c != '')
    classes = []
    # open python modules in user classes directory
    # ex: 'evolacc/userclasses/thing.py' -> 'evolacc.userclasses.thing'
    modules = (dirname.replace('/', '.')+os.path.splitext(f)[0]
               for f in os.listdir(dirname)
               if os.path.splitext(f)[1] == '.py' and f != '__init__.py'
              )
    # collect all expected classes in userclasses list
    for module in modules:
        # import user module
        module = importlib.import_module(module, package=PKG_NAME)
        # collect expected classes
        for attr_name in set(remain_classes):
            if attr_name in module.__dict__.keys():
                attr = module.__getattribute__(attr_name)
                remain_classes.remove(attr_name)
                if class_check(attr):
                    classes.append(attr)
                else:
                    LOGGER.warning("__import_user_classes(): " + attr_name
                                    + " don't verify class_check() predicat"
                                   )
    if len(remain_classes) > 0:
        LOGGER.warning("__import_user_classes(): classes not found: "
              + ','.join((str(g) for g in remain_classes))
        )
    return classes
