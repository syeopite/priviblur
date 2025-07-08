import asyncio

import sanic
import sanic.exceptions

from src.exceptions import exceptions
from src.exceptions.error_handlers import base

miscellaneous_errors = base.ErrorHandlerGroup()


@miscellaneous_errors.register(asyncio.TimeoutError)
async def request_timeout(request, exception):
    return await request.app.ctx.render(
        "misc/msg_error",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": request.app.ctx.translate(
                request.ctx.language, "priviblur_error_request_to_tumblr_timed_out_heading"
            ),
            "error_description": request.app.ctx.translate(
                request.ctx.language, "priviblur_error_request_to_tumblr_timed_out_description"
            ),
        },
        status=504,
    )


@miscellaneous_errors.register(sanic.exceptions.NotFound, IsADirectoryError)
async def error_404(request, exception):
    return await request.app.ctx.render(
        "misc/msg_error",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": "404: Not Found",
            "error_description": f'The requested URL "{request.path}" was not found',
        },
        status=404,
    )


@miscellaneous_errors.register(exceptions.TumblrInvalidRedirect)
async def invalid_redirect(request, exception):
    return await request.app.ctx.render(
        "misc/msg_error",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": request.app.ctx.translate(
                request.ctx.language, "priviblur_error_invalid_internal_tumblr_redirect"
            ),
        },
        status=502,
    )


@miscellaneous_errors.register(Exception)
async def generic_error(request, exception):
    name, message, context = base.create_user_friendly_error_message(request, exception)

    return await request.app.ctx.render(
        "misc/generic_error",
        context={
            "app": request.app,
            "exception": exception,
            "exception_name": name,
            "exception_message": message,
            "exception_context": context,
        },
        status=500,
    )
