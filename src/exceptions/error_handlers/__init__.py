from .extractor_errors import extractor_errors
from .miscellaneous_errors import miscellaneous_errors
from .base import create_user_friendly_error_message


def register(app):
    """Registers all known error handlers into the given Sanic application"""
    extractor_errors.register_handlers_into_app(app)
    miscellaneous_errors.register_handlers_into_app(app)
