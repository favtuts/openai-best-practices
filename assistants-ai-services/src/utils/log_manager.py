import logging
import logging.config

LOGGING_CONFIG = {
    'version': 1,

    'loggers': {
        '': {
            'level': 'DEBUG',
            #'handlers': ['console', 'mail', 'file'],
            'handlers': ['console', 'file'],
        },
        'console': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'info',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'mail': {
            'level': 'ERROR',
            'formatter': 'error',
            'class': 'logging.handlers.SMTPHandler',
            'mailhost': 'localhost',
            'fromaddr': 'monitoring@domain.com',
            'toaddrs': ['dev@domain.com', 'qa@domain.com'],
            'subject': 'Critical error with application name'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/flask.log',
            'maxBytes': 1000000,
            'backupCount': 5,
            'formatter': 'default',
        },
    },

    'formatters': {
        'default': {
            'format': '%(asctime)s | %(levelname)s | %(name)s (%(module)s) | %(lineno)s | %(message)s'
        },
        'info': {
            'format': '%(asctime)s | %(levelname)s | %(name)s (%(module)s) | %(lineno)s | %(message)s'
        },
        'error': {
            'format': '%(asctime)s | %(levelname)s | %(name)s (%(module)s) | %(lineno)s | %(message)s'
        },
    },

}

# Loggers
logging.config.dictConfig(LOGGING_CONFIG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger('sqlalchemy.dialects.postgresql').setLevel(logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

def get_logger(name):
    logger = logging.getLogger(name)
    return logger


########################
# References:
# * https://github.com/chonhan/flask_restapi_clean_architecture/blob/master/extensions/log_extension.py
# * https://github.com/damianoalves/Flask-API/blob/master/app/main/logging.py
########################