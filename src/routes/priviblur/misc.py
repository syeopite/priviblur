import sanic
import sanic_ext

misc_bp = sanic.Blueprint("misc", url_prefix="/")


@misc_bp.get("/licences")
async def licences(request):
    return await request.app.ctx.render(
        "misc/licenses",
        context={
            "app": request.app,
        }
    )