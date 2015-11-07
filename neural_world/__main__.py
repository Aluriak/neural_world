"""

usage:
    __main__.py




"""
from neural_world import commons
from neural_world.world import World
from neural_world.engine import Engine
from neural_world.actions import NextStepAction
from neural_world.incubator import Incubator
from neural_world.world_view import TerminalWorldView


LOGGER = commons.logger()


if __name__ == '__main__':
    i = Incubator()
    w = World(
        width=20, height=20,
        incubator=i,
        nutrient_density=0.8,
        nutrient_regen=0.1,
        indiv_density=0.05,
    )

    e = Engine(w)
    v = TerminalWorldView(e)
    w.register(v)
    w.notify()

    try:
        while True:
            input('next ?')
            e.add(NextStepAction(e))
            e.invoke_all()
    except KeyboardInterrupt:
        LOGGER.info('Treatment loop finished through keyboard interruption.')

