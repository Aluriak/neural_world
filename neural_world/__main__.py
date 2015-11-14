"""

usage:
    __main__.py [options]

options:
    -h, --help          print this help
    -v, --version       print version
    --log-level=LEVEL   log level used for terminal output   [default: warning]
    --render-png=BOOL   activate png files generation        [default: 1]


"""
import time
import docopt

import neural_world.actions as action
from neural_world import commons
from neural_world.info import VERSION
from neural_world.config import Configuration
from neural_world.engine import Engine
from neural_world.observer import (Archivist, TerminalWorldView, TreeBuilder,
                                   InteractiveTerminalWorldView)


LOGGER = commons.logger()
INITIAL_LIFE_COUNT = 4


if __name__ == '__main__':
    # CLI arguments handling
    args = docopt.docopt(__doc__, version=VERSION)
    commons.log_level(args['--log-level'])
    render_png = bool(int(args['--render-png']))

    # Configuration
    config = Configuration()
    assert config.is_valid()

    # Engine from rules
    e = Engine.generate_from(config)

    # Observers
    v = TerminalWorldView(e)
    a = Archivist(commons.DIR_ARCHIVES, simulation_id=int(time.time()),
                  render_graph=render_png)
    t = TreeBuilder(a.archive_directory, render_graph=render_png)
    [e.world.register(_) for _ in (v, a, t)]

    # Initialize the world
    e.world.populate()
    input('next?')

    # Main loop
    try:
        while not config.terminated:
            e.apply(config)
            input('next?')

            if not e.world.have_life:
                # try again, life !
                v.update(e.world)
                for _ in range(INITIAL_LIFE_COUNT):
                    e.add(action.AddAction(config.incubator.spawn()))
                e.world.step_number = 0

    except KeyboardInterrupt:
        LOGGER.info('Treatment loop finished through keyboard interruption.')
    e.world.deinit()
    LOGGER.info('Deinitialization of World')
