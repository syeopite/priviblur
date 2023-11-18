import html
import urllib.parse

import sanic
import sanic_ext

import npf_renderer

from .. import privblur_extractor

tagged = sanic.Blueprint("tagged", url_prefix="/tagged")


@tagged.get("/<tag:str>")
async def _main(request: sanic.Request, tag: str):
    tag = urllib.parse.unquote(tag)
    sort_by = time_filter = request.args.get("sort") or "top"

    if continuation := request.args.get("continuation"):
        continuation = urllib.parse.unquote(continuation)

    if sort_by == "top":
        latest = False
    else:
        latest = True

    initial_results = await request.app.ctx.TumblrAPI.hubs_timeline(tag, continuation=continuation, latest=latest)

    timeline = privblur_extractor.parse_container(initial_results)

    # We remove the continuation parameter used to fetch this page as to ensure the current continuation parameter isn't 
    # added when applying a search filter
    if request.args.get("continuation"):
        del request.args["continuation"]

    return await sanic_ext.render(
        "tagged.jinja",
        context={
            "app": request.app,
            "query_args": request.args,
            "timeline": timeline,
            "tag": tag,
            "sort_by": sort_by
        }
    )