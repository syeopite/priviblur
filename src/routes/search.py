import html
import urllib.parse

import sanic
import sanic_ext

import npf_renderer
from .. import privblur_extractor

search = sanic.Blueprint("search", url_prefix="/search")


async def render_results(app, initial_results, query, url_handler):
        timeline = privblur_extractor.parse_container(initial_results)

        return await sanic_ext.render(
            "search.jinja",
            context={
                "app": app,
                "html_escape": html.escape,
                "url_escape": urllib.parse.quote,
                "timeline": timeline,
                "query": query,
                "url_handler": url_handler,
                "format_npf": npf_renderer.format_npf
            }
        )

@search.get("/")
async def query_param_redirect(request: sanic.Request): 
    """Endpoint for /search to redirect q= queries to /search/<query>"""
    if query := request.args.get("q"):
        return sanic.redirect(request.app.url_for("search._main", query=urllib.parse.quote(query, safe="~")))
    else:
        return sanic.redirect(request.app.url_for("explore._trending"))


@search.get("/<query:str>")
async def _main(request: sanic.Request, query: str):
    query = urllib.parse.unquote(query)
    timeline_type = request.app.ctx.TumblrAPI.config.TimelineType

    if continuation := request.args.get("continuation"):
        continuation = urllib.parse.unquote(continuation)

    initial_results = await request.app.ctx.TumblrAPI.timeline_search(
        query,
        timeline_type.POST,
        continuation=continuation
    )

    return await render_results(request.app, initial_results, query, request.app.ctx.URL_HANDLER)
