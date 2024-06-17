import sanic_ext

from src.exceptions.error_handlers import _base
from src.priviblur_extractor import priviblur_exceptions

extractor_errors = _base.ErrorHandlerGroup()


@extractor_errors.register(priviblur_exceptions.TumblrLoginRequiredError)
async def tumblr_error_login_walled(request, exception):
    return await sanic_ext.render(
        "misc/msg_error.jinja",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": request.app.ctx.translate(request.ctx.language, "tumblr_error_blog_login_required_error_heading"),
            "error_description": request.app.ctx.translate(request.ctx.language, "tumblr_error_blog_login_required_error_description"),
        },
        status=403
    )


@extractor_errors.register(priviblur_exceptions.TumblrRestrictedTagError)
async def tumblr_error_restricted_tag(request, exception):
    return await sanic_ext.render(
        "misc/msg_error.jinja",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": request.app.ctx.translate(request.ctx.language, "tumblr_error_restricted_tag_error_heading"),
            "error_description": request.app.ctx.translate(request.ctx.language, "tumblr_error_restricted_tag_description"),
        },
        status=403
    )


@extractor_errors.register(priviblur_exceptions.TumblrBlogNotFoundError)
async def tumblr_error_unknown_blog(request, exception):
    return await sanic_ext.render(
        "misc/msg_error.jinja",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": request.app.ctx.translate(request.ctx.language, "tumblr_error_blog_not_found_error_heading"),
            "error_description": request.app.ctx.translate(request.ctx.language, "tumblr_error_blog_not_found_error_description"),
        },
        status=404
    )
