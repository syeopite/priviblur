import html
import urllib.parse

import sanic
import sanic_ext

import npf_renderer

from .. import privblur_extractor

tagged = sanic.Blueprint("tagged", url_prefix="/tagged")


async def render_results(app, initial_results, tag, url_handler):
        timeline = privblur_extractor.parse_container(initial_results)

        return await sanic_ext.render(
            "tagged.jinja",
            context={
                "app": app,
                "html_escape": html.escape,
                "url_escape": urllib.parse.quote,
                "timeline": timeline,
                "tag": tag,
                "url_handler": url_handler,
                "format_npf": npf_renderer.format_npf
            }
        )

@tagged.get("/<tag:str>")
async def _main(request: sanic.Request, tag: str):
    tag = urllib.parse.unquote(tag)

    if continuation := request.args.get("continuation"):
        continuation = urllib.parse.unquote(continuation)

    initial_results = await request.app.ctx.TumblrAPI.hubs_timeline(
        tag,
        continuation=continuation
    )

    return await render_results(request.app, initial_results, tag, request.app.ctx.URL_HANDLER)
