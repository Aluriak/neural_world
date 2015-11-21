"""
Definitions of Actions class, which are designed to be applied
 on a World object instance.

Define also the ActionEmitter base class, which is mostly designed
 for simplifications of Action emission.

"""
import neural_world.commons as commons
from neural_world.commons import Direction


LOGGER = commons.logger('life')


class ActionEmitter:
    """ActionEmitters is a base class which provides an API
    to send actions to the invoker"""

    def __init__(self, invoker):
        self.invoker = invoker

    def emit(self, action):
        self.invoker.add(action)


class Action:

    def __init__(self):
        pass

    def execute(self, world):
        raise NotImplementedError

    def undo(self, world):
        raise NotImplementedError


class MoveAction(Action):

    def __init__(self, obj, coords, directions):
        self.obj = obj
        self.coords = coords
        self.directions = directions

    def execute(self, world):
        world.move(self.obj, self.coords, self.directions)


class PickNutrientAction(Action):

    def __init__(self, indiv, coords):
        self.indiv, self.coords = indiv, coords

    def execute(self, world):
        world.pick_nutrient(self.indiv, self.coords)


class ReplicateAction(Action):

    def __init__(self, obj, coords):
        self.obj, self.coords = obj, coords

    def execute(self, world):
        world.spawn_from(self.obj, self.coords)


class RemoveAction(Action):

    def __init__(self, obj, coords):
        self.obj = obj
        self.coords = coords

    def execute(self, world):
        world.remove(self.obj, self.coords)


class AddAction(Action):

    def __init__(self, obj, coords=None):
        self.obj = obj
        self.coords = coords

    def execute(self, world):
        if self.coords is None:
            world.add(self.obj, world.random_coords())
        else:
            world.add(self.obj, self.coords)


class StepComputedAction(Action):

    def execute(self, world):
        world.step_number += 1
        world.notify_observers()


class RegenerateNutrientsAction(Action):

    def execute(self, world):
        world.regenerate_nutrient()

class QuitAction(Action):

    def execute(self, world):
        world.config.terminated = True
