import urllib.parse

import sanic

from ....cache import get_poll_results

misc = sanic.Blueprint("api_misc", url_prefix="/")


@misc.get(r"/poll/<blog:([a-z\d]{1}[a-z\d-]{0,30}[a-z\d]{0,1})>/<post_id:int>/<poll_id:str>/results")
async def poll_results(request, blog: str, post_id: int, poll_id: int):
    blog = urllib.parse.unquote(blog)
    poll_id = urllib.parse.unquote(poll_id)

    expired = request.args.get("expired")

    initial_results = await get_poll_results(
        ctx=request.app.ctx, blog=blog, post_id=post_id, poll_id=poll_id, expired=bool(expired)
    )

    return sanic.response.json(initial_results, headers={"Cache-Control": "max-age=600, immutable"})
