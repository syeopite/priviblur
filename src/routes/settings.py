import sanic
import sanic_ext

import urllib.parse

settings = sanic.Blueprint("settings", url_prefix="/settings")


@settings.get("/")
async def settings_page(request):
    return await request.app.ctx.render(
        "settings",
        context={
            "app": request.app,
        }
    )


@settings.post("/")
async def settings_post(request):
    request.ctx.preferences = request.ctx.preferences.replace_from_forms(request)

    response = await request.app.ctx.render(
        "settings",
        context={
            "app": request.app,
        }
    )

    response.add_cookie(
        **request.ctx.preferences.construct_cookie(request)
    )

    request.ctx.invalid_settings_cookie = False

    return response

@settings.get("/restore")
async def settings_restore(request):
    request.ctx.preferences = request.ctx.preferences.replace_from_query(request)

    response = await request.app.ctx.render(
        "settings",
        context={
            "app": request.app,
        }
    )

    response.add_cookie(
        **request.ctx.preferences.construct_cookie(request)
    )

    request.ctx.invalid_settings_cookie = False

    return response