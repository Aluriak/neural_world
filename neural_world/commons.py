"""
Defines global values, types and access to the logger.

"""
import logging
import logging.config
import logging.handlers
import itertools
from enum import Enum, IntEnum
from functools import reduce
from collections import Counter
from logging.handlers import RotatingFileHandler

from neural_world.info import PACKAGE_NAME


# DIRECTORIES AND FILES
DIR_PACKAGE  = PACKAGE_NAME + '/'
DIR_LOGS     = DIR_PACKAGE + 'logs/'
DIR_ASP      = DIR_PACKAGE + 'asp/'
DIR_ARCHIVES = DIR_PACKAGE + 'archives/'
ASP_SOLVING  = DIR_ASP + 'neural_solving.lp'
ASP_CLEANING = DIR_ASP + 'network_cleaning.lp'
# LOGGER CONSTANTS
LOGGER_NAME = PACKAGE_NAME
LOG_LEVEL   = logging.DEBUG
MAIN_LOGGER = logging.getLogger(LOGGER_NAME)
SUBLOGGER_SOLVING = 'solving'
SUBLOGGER_LIFE    = 'life'
SUBLOGGER_SEPARATOR = '_'  # '.' for allowing inheritance
LOGFILE_MAX_SIZE  = 2**20
# ASP SOLVING OPTIONS
ASP_GRINGO_OPTIONS = ''  # no default options
ASP_CLASP_OPTIONS  = ''  # options of solving heuristics
# ASP_CLASP_OPTIONS += ' -Wno-atom-undefined'
# ASP_CLASP_OPTIONS += ' --configuration=frumpy'
# ASP_CLASP_OPTIONS += ' --heuristic=Vsids'



# TYPES DEFINITION
class Direction(IntEnum):
    "Enumeration of the four possible movement directions"
    up, right, down, left = 0, 1, 2, 3

    @property
    def opposite(self):
        "Return the opposite of self"
        return Direction((self + 2) % 4)

    def is_opposite(self, othr) -> bool:
        "True if self and other are opposites"
        return self.opposite is othr

    @staticmethod
    def neighbor(coords, direction):
        "Return the neighbor coordinates of given coords, in given direction"
        x, y = coords
        if   direction is Direction.up:    return x    , y - 1
        elif direction is Direction.right: return x + 1, y
        elif direction is Direction.down:  return x    , y + 1
        elif direction is Direction.left:  return x - 1, y

    @staticmethod
    def final_coords(coords, directions):
        "Coords reached after moves in given directions from given coords"
        return tuple(reduce(Direction.neighbor,
                     itertools.chain([coords], directions)))

    @staticmethod
    def simplified(directions):
        "Return an iterable of directions, that is in absolute equivalent to the given one"
        c = Counter(directions)
        sum_up = c[Direction.up] - c[Direction.down]
        dir_up = Direction.up if sum_up > 0 else Direction.down
        sum_left = c[Direction.left] - c[Direction.right]
        dir_left = Direction.left if sum_left > 0 else Direction.right
        return itertools.chain(
            itertools.repeat(dir_up, times=abs(sum_up)),
            itertools.repeat(dir_left, times=abs(sum_left)),
        )

    def __str__(self):
        return self.name

assert     Direction.up.is_opposite(Direction.down)
assert     Direction.left.is_opposite(Direction.right)
assert not Direction.up.is_opposite(Direction.right)
assert     Direction.left.opposite is Direction.right
assert     Direction.down.opposite is Direction.up
assert not Direction.left.opposite is Direction.up


class NeuronType(Enum):
    """Type of a Neuron is in IXANO"""
    INPUT = 'i'
    XOR   = 'x'
    AND   = 'a'
    NOT   = 'n'
    OR    = 'o'

    @staticmethod
    def ixano(): return tuple(e for e in NeuronType)
    @staticmethod
    def xano(): return tuple(e for e in NeuronType
                             if e is not NeuronType.INPUT)

assert ''.join(e.value for e in NeuronType.ixano())== NeuronType.ixano.__name__
assert ''.join(e.value for e in NeuronType.xano()) == NeuronType.xano.__name__


# LOGGING DEFINITION
def logger(name=None, logfilename=None):
    """Return logger of the package, without initialize it.

    If name is provided, a sublogger PACKAGE_NAME.name will be returned.
    Equivalent of logging.getLogger() call.
    """
    assert logging.getLogger(LOGGER_NAME) == MAIN_LOGGER
    if name:
        return logging.getLogger(LOGGER_NAME + SUBLOGGER_SEPARATOR + name)
    else:
        return logging.getLogger(LOGGER_NAME)  # equivalent to main logger

def log_level(level=None, name=None):
    """Set terminal log level to given one, or return the current
    loglevel if None is given."""
    target_logger = logger(name)  # get target logger
    handlers = (_ for _ in target_logger.handlers
                if _.__class__ is logging.StreamHandler)
    if level:
        for handler in handlers:
            handler.setLevel(level.upper())
        return level
    else:
        levels = Counter(h.level for h in handlers)
        return max(levels)

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'console':{
            'level':LOG_LEVEL,
            'class':'logging.StreamHandler',
            'formatter': 'simple',
        },
        'logfile': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': DIR_LOGS + LOGGER_NAME + '.log',
            'mode': 'w',
            'maxBytes': LOGFILE_MAX_SIZE,
            'formatter': 'verbose',
        },
        'logfile' + SUBLOGGER_SEPARATOR + SUBLOGGER_SOLVING: {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': DIR_LOGS + LOGGER_NAME + '.' + SUBLOGGER_SOLVING + '.log',
            'mode': 'w',
            'maxBytes': LOGFILE_MAX_SIZE,
            'formatter': 'verbose',
        },
        'logfile' + SUBLOGGER_SEPARATOR + SUBLOGGER_LIFE: {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': DIR_LOGS + LOGGER_NAME + '.' + SUBLOGGER_LIFE + '.log',
            'mode': 'w',
            'maxBytes': LOGFILE_MAX_SIZE,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        PACKAGE_NAME: {
            'handlers':['console', 'logfile'],
            'propagate': True,
            'level':LOG_LEVEL,
        },
        PACKAGE_NAME + '_solving': {
            'handlers':['logfile' + SUBLOGGER_SEPARATOR + SUBLOGGER_SOLVING],
            'level':LOG_LEVEL,
        },
        PACKAGE_NAME + '_life': {
            'handlers':['logfile' + SUBLOGGER_SEPARATOR + SUBLOGGER_LIFE],
            'level':LOG_LEVEL,
        },
    }
})

