import html
import urllib.parse

import sanic
import sanic_ext

import npf_renderer

from .. import privblur_extractor

explore = sanic.Blueprint("explore", url_prefix="/explore")


async def _handle_explore(request, endpoint, post_type = None):
    app = request.app
    raw_endpoint = endpoint
    endpoint = request.app.url_for(endpoint)

    if continuation := request.args.get("continuation"):
        continuation = urllib.parse.unquote(continuation)

    match raw_endpoint:
        case "explore._trending":
            initial_results = await request.app.ctx.TumblrAPI.explore_trending(continuation=continuation)
        case "explore._today":
            initial_results = await request.app.ctx.TumblrAPI.explore_today(continuation=continuation)
        case _:
            initial_results = await request.app.ctx.TumblrAPI.explore_post(post_type=post_type, continuation=continuation)        

    timeline = privblur_extractor.parse_container(initial_results)

    return await sanic_ext.render(
        "explore.jinja",
        context={
            "app": app,
            "endpoint": endpoint,
            "html_escape": html.escape,
            "url_escape": urllib.parse.quote,
            "url_handler": app.ctx.URL_HANDLER,
            "timeline": timeline,
            "format_npf": npf_renderer.format_npf
        }
    )


@explore.get("/")
async def _main(request):
    return sanic.redirect(request.app.url_for("explore._trending"))  # /explore/trending


@explore.get("/trending")
async def _trending(request):
    return await _handle_explore(request, "explore._trending")

@explore.get("/today")
async def _today(request):
    return await _handle_explore(request, "explore._today")

@explore.get("/today/json")
async def _today_json(request):
    if continuation := request.args.get("continuation"):
        continuation = urllib.parse.unquote(continuation)
    else:
        continuation = None


    initial_results = await request.app.ctx.TumblrAPI.explore_today(continuation=continuation)
    return sanic.response.json(initial_results)


@explore.get("/text")
async def _text(request):
    return await _handle_explore(request, "explore._text", request.app.ctx.TumblrAPI.config.PostType.TEXT)


@explore.get("/photos")
async def _photos(request):
    return await _handle_explore(request, "explore._photos", request.app.ctx.TumblrAPI.config.PostType.PHOTOS)


@explore.get("/gifs")
async def _gifs(request):
    return await _handle_explore(request, "explore._gifs", request.app.ctx.TumblrAPI.config.PostType.GIFS)


@explore.get("/quotes")
async def _quotes(request):
    return await _handle_explore(request, "explore._quotes", request.app.ctx.TumblrAPI.config.PostType.QUOTES)


@explore.get("/chats")
async def _chats(request):
    return await _handle_explore(request, "explore._chats", request.app.ctx.TumblrAPI.config.PostType.CHATS)


@explore.get("/asks")
async def _asks(request):
    return await _handle_explore(request, "explore._asks", request.app.ctx.TumblrAPI.config.PostType.ASKS)
