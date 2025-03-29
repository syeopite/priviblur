import sanic.log


def setup_logging(logging_config):
    """Setup Sanic's logging configuration"""
    sanic_logging_config = sanic.log.LOGGING_CONFIG_DEFAULTS.copy()

    # Set Sanic's own logging to the desired logging level
    for logger in sanic_logging_config["loggers"].values():
        logger["level"] = logging_config.sanic_logging_level

    # Define new handler and formatter
    # Defines generic "priviblur_generic_console" handler
    _define_generic_handler_and_formatter(sanic_logging_config)

    sanic_logging_config["loggers"]["priviblur"] = {
        "level": logging_config.priviblur_logging_level,
        "handlers": ["priviblur_generic_console"],
        "propagate": True,
        "qualname": "priviblur",
    }

    sanic_logging_config["loggers"]["priviblur-extractor"] = {
        "level": logging_config.priviblur_extractor_logging_level,
        "handlers": ["priviblur_generic_console"],
        "propagate": True,
        "qualname": "priviblur-extractor",
    }

    return sanic_logging_config


def _define_generic_handler_and_formatter(sanic_logging_config):
    priviblur_generic_handler = sanic_logging_config["handlers"]["console"].copy()

    # Add handler and format to config
    formatter = _define_generic_formatter(sanic_logging_config)
    sanic_logging_config["formatters"]["priviblur_generic"] = formatter

    sanic_logging_config["handlers"]["priviblur_generic_console"] = priviblur_generic_handler
    sanic_logging_config["handlers"]["priviblur_generic_console"]["formatter"] = "priviblur_generic"


def _define_generic_formatter(sanic_logging_config):
    formatter = sanic_logging_config["formatters"]["generic"].copy()
    formatter["format"] = "%(asctime)s - (%(name)s) [%(process)d] [%(levelname)s]: %(message)s "

    return formatter
