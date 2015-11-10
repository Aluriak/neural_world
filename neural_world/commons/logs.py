"""
Definition and application of logging configuration.

"""
import logging
import logging.config
import logging.handlers

from collections import Counter
from logging.handlers import RotatingFileHandler

from .commons import DIR_LOGS, PACKAGE_NAME


# LOGGER CONSTANTS
LOGGER_NAME = PACKAGE_NAME
LOG_LEVEL   = logging.DEBUG
MAIN_LOGGER = logging.getLogger(LOGGER_NAME)
SUBLOGGER_SOLVING = 'solving'
SUBLOGGER_LIFE    = 'life'
SUBLOGGER_SEPARATOR = '_'  # '.' for allowing inheritance
LOGFILE_MAX_SIZE  = 2**20


# API Functions
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

# Logging configuration
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

