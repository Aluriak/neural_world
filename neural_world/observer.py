"""
Definition of Observer and Observable mother classes,
and of all signals passing between them.

"""
from enum import Enum


class signal(Enum):
    """Enumeration of all signals constants"""
    NEW_STEP = 1
    NEW_INDIVIDUAL = 2


class Observer:
    """Receive signals from an Observable"""

    def update(self, observable, signals):
        """Print World in the terminal"""
        pass


class Observable:
    """Emit signals to its Observers"""

    def __init__(self):
        self.observers = set()

    def register(self, observer):
        "Add given observer to set of observers"
        self.observers.add(observer)

    def unregister(self, observer):
        "Remove given observer from set of observers"
        self.observers.remove(observer)

    def notify_observers(self, signals={}):
        "notify all observers"
        [o.update(self, signals) for o in self.observers]

