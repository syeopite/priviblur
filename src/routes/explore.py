import sanic
import sanic.response

explore = sanic.Blueprint("explore", url_prefix="/explore")


@explore.get("/")
async def _main(_):
    return sanic.response.empty()
