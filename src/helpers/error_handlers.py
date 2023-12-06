import sanic
import sanic_ext

async def tumblr_error_login_walled(request, exception):
    return await sanic_ext.render(
        "misc/generic_error.jinja",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": request.app.ctx.translate("en", "tumblr_error_blog_login_required_error_heading"),
            "error_description": request.app.ctx.translate("en", "tumblr_error_blog_login_required_error_description"),
        }
    )


async def tumblr_error_restricted_tag(request, exception):
    return await sanic_ext.render(
        "misc/generic_error.jinja",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": request.app.ctx.translate("en", "tumblr_error_restricted_tag_error_heading"),
            "error_description": request.app.ctx.translate("en", "tumblr_error_restricted_tag_description"),
        }
    )

async def tumblr_error_unknown_blog(request, exception):
    return await sanic_ext.render(
        "misc/generic_error.jinja",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": request.app.ctx.translate("en", "tumblr_error_blog_not_found_error_heading"),
            "error_description": request.app.ctx.translate("en", "tumblr_error_blog_not_found_error_description"),
        }
    )


async def request_timeout(request, exception):
    return await sanic_ext.render(
        "misc/generic_error.jinja",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": request.app.ctx.translate("en", "priviblur_error_request_to_tumblr_timed_out_heading"),
            "error_description": request.app.ctx.translate("en", "priviblur_error_request_to_tumblr_timed_out_description")
        },
        status=504
    )


async def pool_timeout_error(request, exception):
    return await sanic_ext.render(
        "misc/generic_error.jinja",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": request.app.ctx.translate("en", "priviblur_error_pool_timeout_error_heading"),
            "error_description": request.app.ctx.translate("en", "priviblur_error_pool_timeout_error_description")
        },
        status=504
    )


async def error_404(request, exception):
    return await sanic_ext.render(
        "misc/generic_error.jinja",
        context={
            "app": request.app,
            "exception": exception,
            "error_heading": "404: Not Found",
            "error_description": f"The requested URL \"{request.path}\" was not found",
        }
    )
