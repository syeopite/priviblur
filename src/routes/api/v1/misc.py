import urllib.parse

import sanic

misc = sanic.Blueprint("api_misc", url_prefix="/")

@misc.get("/poll/<blog:([a-z\d]{1}[a-z\d-]{0,30}[a-z\d]{0,1})>/<post_id:int>/<poll_id:str>/results")
async def poll_results(request, blog : str, post_id : int, poll_id : int):
    blog = urllib.parse.unquote(blog)
    poll_id = urllib.parse.unquote(poll_id)

    initial_results = await request.app.ctx.TumblrAPI.poll_results(blog, post_id, poll_id)
    return sanic.response.json(initial_results)