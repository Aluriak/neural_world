"""
Invoker of actions, from View onto World.

"""
import neural_world.commons as commons
import neural_world.actions as action
from neural_world.world import World
from neural_world.commons import coroutine


LOGGER = commons.logger()


class Engine:

    def __init__(self, world):
        self.world = world
        self.commands = []

    def add(self, command):
        try:
            [self.commands.append(c) for c in command]
        except TypeError:
            self.commands.append(command)

    def invoke_all(self):
        [c.execute(self.world) for c in self.commands]
        self.commands = []

    def apply(self, config):
        """Apply given config then wait for the next."""
        if not config.terminated:
            # prepare the next amount of actions
            for coords, obj in self.world:
                obj.update(self, self.world.neighbors(coords), coords)
            self.add(action.RegenerateNutrientsAction())
            self.add(action.StepComputedAction())
            # invoke them
            self.invoke_all()

    @staticmethod
    def generate_from(config):
        """Generate world according to config."""
        world = World(config)
        return Engine(world)


