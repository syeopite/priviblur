import logging

import sanic.log


def setup_logging(config):
    """Setup Sanic's logging configuration"""
    sanic_logging_config = sanic.log.LOGGING_CONFIG_DEFAULTS.copy()

    # Set Sanic's own logging to the desired logging level
    for logger in sanic_logging_config["loggers"].values():
        logger["level"] = config["sanic_logging_level"]

    # Define new handler and formatter
    privblur_generic_handler = sanic_logging_config["handlers"]["console"].copy()
    formatter = sanic_logging_config["formatters"]["generic"].copy()
    formatter["format"] = "%(asctime)s - (%(name)s) [%(process)d] [%(levelname)s]: %(message)s "

    # Add handler and format to config
    sanic_logging_config["formatters"]["privblur_generic"] = formatter  

    sanic_logging_config["handlers"]["privblur_generic_console"] = privblur_generic_handler
    sanic_logging_config["handlers"]["privblur_generic_console"]["formatter"] = "privblur_generic"

    sanic_logging_config["loggers"]["privblur"] = {
        "level": config["privblur_logging_level"],
        'handlers': ['privblur_generic_console'],
        'propagate': True,
        'qualname': 'privblur'
    }

    sanic_logging_config["loggers"]["privblur-extractor"] = {
        "level": config["privblur_extractor_logging_level"],
        'handlers': ['privblur_generic_console'],
        'propagate': True,
        'qualname': 'privblur-extractor'
    }

    return sanic_logging_config
