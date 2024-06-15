class ErrorHandlerGroup:
    """Manages and registers error handler functions for specific exceptions

    A ErrorHandlerGroup stores error handling functions and its triggering
    exceptions via the `register()` decorator

    These functions are then registered into Sanic via the
    `register_handlers_into_app()` method.

    This is primary used to organize exception handlers in the codebase.
    """
    def __init__(self) -> None:
        self.registered_handlers = {}

    def register(self, *attached_exceptions):
        """Decorator used to register an exception handler into the ErrorHandlerGroup instance"""
        def registrator(target_handler):
            self.registered_handlers[target_handler] = attached_exceptions

        return registrator

    def register_handlers_into_app(self, app):
        """Registers the tracked exception handlers into the given Sanic app"""
        for handler, exceptions in self.registered_handlers.items():
            for exception in exceptions:
                app.error_handler.add(exception, handler)
