"""

usage:
    __main__.py [options]

options:
    -h, --help          print this help
    -v, --version       print version
    --log-level=LEVEL   log level used for terminal output [default: warning]


"""
import time
import docopt

from neural_world import commons
from neural_world.info import VERSION
from neural_world.world import World
from neural_world.engine import Engine
from neural_world.mutator import Mutator
from neural_world.actions import NextStepAction, AddAction
from neural_world.incubator import Incubator
from neural_world.world_view import TerminalWorldView


LOGGER = commons.logger()


if __name__ == '__main__':
    # CLI arguments handling
    args = docopt.docopt(__doc__, version=VERSION)
    commons.log_level(args['--log-level'])


    # Individual Factory
    m = Mutator(mutation_rate=0.2)
    i = Incubator(m)

    # World
    w = World(
        width=20, height=20,
        incubator=i,
        nutrient_density=0.8,
        nutrient_regen=0.005,
        indiv_count=4,
    )

    # Engine and View
    e = Engine(w)
    v = TerminalWorldView(e)
    w.register(v)

    # Initialize the world
    w.populate()

    try:
        w.notify_observers()
        while True:
            while w.have_life:
                time.sleep(0.5)
                e.add(NextStepAction(e))
                e.invoke_all()
            # try again, life !
            v.update(w)
            for _ in range(4):
                e.add(AddAction(i.spawn()))
            e.invoke_all()
            w.step_number = 0
    except KeyboardInterrupt:
        LOGGER.info('Treatment loop finished through keyboard interruption.')
