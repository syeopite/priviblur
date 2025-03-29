import sanic_ext

from src.exceptions.error_handlers import base
from src.priviblur_extractor import priviblur_exceptions

extractor_errors = base.ErrorHandlerGroup()


@extractor_errors.register(priviblur_exceptions.TumblrLoginRequiredError)
async def tumblr_error_login_walled(request, exception):
    return await request.app.ctx.render(
        "misc/msg_error",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": request.app.ctx.translate(
                request.ctx.language, "tumblr_error_blog_login_required_error_heading"
            ),
            "error_description": request.app.ctx.translate(
                request.ctx.language, "tumblr_error_blog_login_required_error_description"
            ),
        },
        status=403,
    )


@extractor_errors.register(priviblur_exceptions.TumblrPasswordRequiredBlogError)
async def tumblr_password_required_blog(request, exception):
    return await request.app.ctx.render(
        "misc/msg_error",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": request.app.ctx.translate(
                request.ctx.language, "tumblr_error_blog_requires_password_error_heading"
            ),
            "error_description": request.app.ctx.translate(
                request.ctx.language, "tumblr_error_blog_login_required_error_description"
            ),
        },
        status=403,
    )


@extractor_errors.register(priviblur_exceptions.TumblrRestrictedTagError)
async def tumblr_error_restricted_tag(request, exception):
    return await request.app.ctx.render(
        "misc/msg_error",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": request.app.ctx.translate(
                request.ctx.language, "tumblr_error_restricted_tag_error_heading"
            ),
            "error_description": request.app.ctx.translate(
                request.ctx.language, "tumblr_error_restricted_tag_description"
            ),
        },
        status=403,
    )


@extractor_errors.register(priviblur_exceptions.TumblrBlogNotFoundError)
async def tumblr_error_unknown_blog(request, exception):
    return await request.app.ctx.render(
        "misc/msg_error",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": request.app.ctx.translate(
                request.ctx.language, "tumblr_error_blog_not_found_error_heading"
            ),
            "error_description": request.app.ctx.translate(
                request.ctx.language, "tumblr_error_blog_not_found_error_description"
            ),
        },
        status=404,
    )


@extractor_errors.register(priviblur_exceptions.TumblrNon200NorJSONResponse)
async def tumblr_error_debug_non_json_response_error(request, exception):
    return await request.app.ctx.render(
        "misc/msg_error",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": f"Non 200 status code. Tumblr returned {exception.status_code} ",
            "error_description": "Priviblur might have been ratelimited by Tumblr. Please try again later.",
        },
        status=500,
    )


@extractor_errors.register(priviblur_exceptions.TumblrRatelimitReachedError)
async def tumblr_error_ratelimit(request, exception):
    return await request.app.ctx.render(
        "misc/msg_error",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": request.app.ctx.translate(
                request.ctx.language, "tumblr_error_ratelimit_reached_heading"
            ),
            "error_description": request.app.ctx.translate(
                request.ctx.language, "tumblr_error_ratelimit_reached_description"
            ),
        },
        status=429,
    )
