import sanic
import sanic_ext

import urllib.parse

settings = sanic.Blueprint("settings", url_prefix="/settings")


@settings.get("/")
async def settings_page(request):
    return await sanic_ext.render(
        "settings.jinja",
        context={
            "app": request.app,
        }
    )


@settings.post("/")
async def settings_post(request):
    request.ctx.preferences.update_from_request(request)

    response = await sanic_ext.render(
        "settings.jinja",
        context={
            "app": request.app,
        }
    )

    response.add_cookie(
        **request.ctx.preferences.to_cookie(request)
    )

    return response