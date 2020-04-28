''' Logging info, debug with coloredlogs '''
import logging.config

from coloredlogs import ColoredFormatter

CONFIG = {
    "version": 1,
    'disable_existing_loggers': False,
    "formatters": {
        "colored": {
            "()": ColoredFormatter,
            'format': "%(asctime)s [%(name)s L%(lineno)s] %(levelname)s:  %(message)s",
            'datefmt': '%m/%d/%Y %H:%M:%S'
        },
        "standard": {
            'format': "%(asctime)s [%(name)s L%(lineno)s] %(levelname)s: %(message)s",
            'datefmt': '%m/%d/%Y %H:%M:%S'
        }
    },
    "handlers": {
        "infoHandler": {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
            'stream': 'ext://sys.stdout'
        },
        'debugHandler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': 'debug.log',
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['debugHandler', 'infoHandler']
        }
    }
}


def setup_logger():
    """Setup logger with appropriate configuration."""
    logging.config.dictConfig(CONFIG)
