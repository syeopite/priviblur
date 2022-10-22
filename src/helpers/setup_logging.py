import logging

import sanic.log


def setup_logging(selected_log_level=logging.WARN):
    """Setup Sanic's logging configuration"""
    sanic_logging_config = sanic.log.LOGGING_CONFIG_DEFAULTS.copy()

    # Set Sanic's own logging to the desired logging level
    for logger in sanic_logging_config["loggers"].values():
        logger["level"] = selected_log_level

    # First we register a custom formatter since we want to know the loggers name in our logs in order to know
    # where it comes from
    privblur_generic_handler = sanic_logging_config["handlers"]["console"].copy()
    formatter = sanic_logging_config["formatters"]["generic"].copy()

    privblur_generic_handler["formatter"] = "privblur_generic"
    sanic_logging_config["handlers"]["privblur_generic_console"] = privblur_generic_handler

    formatter["format"] = "%(asctime)s - (%(name)s) [%(process)d] [%(levelname)s]: %(message)s "
    sanic_logging_config["formatters"]["privblur_generic"] = formatter

    # Now we configure the primary logger
    sanic_logging_config["loggers"]["privblur"] = {
        "level": selected_log_level,
        'handlers': ['console'],
        'propagate': True,
        'qualname': 'privblur'
    }

    # And then the libraries we care about
    sanic_logging_config["loggers"]["privblur-extractor"] = {
        "level": selected_log_level,
        'handlers': ['privblur_generic_console'],
        'propagate': True,
        'qualname': 'privblur-extractor'
    }

    return sanic_logging_config
