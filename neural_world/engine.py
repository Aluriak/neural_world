"""
Invoker of actions, from View onto World.

"""


class Engine:

    def __init__(self, world):
        self.world = world
        self.commands = []

    def add(self, command):
        self.commands.append(command)

    def invoke_all(self):
        [c.execute(self.world) for c in self.commands]
        self.commands = []
        self.world.notify()


