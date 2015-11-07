"""
Definitions of Actions class, which are designed to be applied
 on a World object instance.

"""
import neural_world.commons as commons
from neural_world.commons import Direction


LOGGER = commons.logger()


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
        world.remove(self.obj, self.coords)
        final_coords = Direction.final_coords(self.coords, self.directions)
        world.add(self.obj, final_coords)
        # pick nutrients if possible
        if self.obj.is_individual:
            self.obj.energy += world.consume_nutrient(final_coords)
            LOGGER.debug('CONSUME NUTRIENTS: ' + str(self.obj))
        LOGGER.debug('MOVE: ' + str(self.obj) + ': ' + str(self.coords) + ' -> '
                     + str(self.directions) + ' -> ' + str(final_coords))


class RemoveAction(Action):

    def __init__(self, obj, coords):
        self.obj = obj
        self.coords = coords

    def execute(self, world):
        world.remove(self.obj, self.coords)


class AddAction(Action):

    def __init__(self, obj, coords):
        self.obj = obj
        self.coords = coords

    def execute(self, world):
        world.add(self.obj, self.coords)


class NextStepAction(Action):

    def __init__(self, engine, count=1):
        self.engine = engine
        self.count = count

    def execute(self, world):
        for coords, obj in world:
            obj.update(self.engine, world.neighbors(coords), coords)
