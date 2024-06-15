import asyncio

import sanic
import sanic.exceptions
import sanic_ext

from src.helpers import exceptions
from src.error_handlers import _base

miscellaneous_errors = _base.ErrorHandlerGroup()


@miscellaneous_errors.register(asyncio.TimeoutError)
async def request_timeout(request, exception):
    return await sanic_ext.render(
        "misc/msg_error.jinja",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": request.app.ctx.translate(request.ctx.language, "priviblur_error_request_to_tumblr_timed_out_heading"),
            "error_description": request.app.ctx.translate(request.ctx.language, "priviblur_error_request_to_tumblr_timed_out_description")
        },
        status=504
    )


@miscellaneous_errors.register(sanic.exceptions.NotFound)
async def error_404(request, exception):
    return await sanic_ext.render(
        "misc/msg_error.jinja",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": "404: Not Found",
            "error_description": f"The requested URL \"{request.path}\" was not found",
        },
    status=404
    )


@miscellaneous_errors.register(exceptions.TumblrInvalidRedirect)
async def invalid_redirect(request, exception):
    return await sanic_ext.render(
        "misc/msg_error.jinja",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": request.app.ctx.translate(request.ctx.language, "priviblur_error_invalid_internal_tumblr_redirect"),
        },
    status=502
    )
