import sanic
import sanic_ext

settings = sanic.Blueprint("settings", url_prefix="/settings")


@settings.get("/")
async def settings_page(request):
    return await sanic_ext.render(
        "settings.jinja",
        context={
            "app": request.app,
        }
    )
