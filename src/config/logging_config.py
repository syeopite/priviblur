from typing import NamedTuple


class LoggingConfig(NamedTuple):
    """NamedTuple that stores configuration values relating to logging

    Attributes:
        sanic_logging_level:
            Numerical log level for the underlying server framework (Sanic)
        priviblur_logging_level:
            Numerical log level for priviblur
        priviblur_extractor_logging_level:
            Numerical log level for priviblur's extractor backend
    """

    sanic_logging_level: int = 50
    priviblur_logging_level: int = 30
    priviblur_extractor_logging_level: int = 30
