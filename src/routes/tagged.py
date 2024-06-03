import html
import urllib.parse

import sanic
import sanic_ext

from .. import priviblur_extractor
from ..cache import get_tag_browse_results

tagged = sanic.Blueprint("tagged", url_prefix="/tagged")


@tagged.get("/<tag:str>")
async def _main(request: sanic.Request, tag: str):
    tag = urllib.parse.unquote(tag)
    sort_by = request.args.get("sort")

    if continuation := request.args.get("continuation"):
        continuation = urllib.parse.unquote(continuation)

    latest = False
    if sort_by == "recent":
        latest = True
    else:
        sort_by = "top"

    timeline = await get_tag_browse_results(request.app.ctx, tag, latest=latest, continuation=continuation)

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