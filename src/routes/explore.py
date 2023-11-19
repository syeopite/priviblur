import html
import urllib.parse

import sanic
import sanic_ext

import npf_renderer

from .. import priviblur_extractor

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

    timeline = priviblur_extractor.parse_container(initial_results)

    return await sanic_ext.render(
        "explore.jinja",
        context={
            "app": app,
            "timeline": timeline,
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

@explore.get("/text")
async def _text(request):
    return await _handle_explore(request, "explore._text", request.app.ctx.TumblrAPI.config.ExplorePostTypeFilters.TEXT)


@explore.get("/photos")
async def _photos(request):
    return await _handle_explore(request, "explore._photos", request.app.ctx.TumblrAPI.config.ExplorePostTypeFilters.PHOTOS)


@explore.get("/gifs")
async def _gifs(request):
    return await _handle_explore(request, "explore._gifs", request.app.ctx.TumblrAPI.config.ExplorePostTypeFilters.GIFS)


@explore.get("/quotes")
async def _quotes(request):
    return await _handle_explore(request, "explore._quotes", request.app.ctx.TumblrAPI.config.ExplorePostTypeFilters.QUOTES)


@explore.get("/chats")
async def _chats(request):
    return await _handle_explore(request, "explore._chats", request.app.ctx.TumblrAPI.config.ExplorePostTypeFilters.CHATS)


@explore.get("/audio")
async def _audio(request):
    return await _handle_explore(request, "explore._audio", request.app.ctx.TumblrAPI.config.ExplorePostTypeFilters.AUDIO)


@explore.get("/videos")
async def _videos(request):
    return await _handle_explore(request, "explore._videos", request.app.ctx.TumblrAPI.config.ExplorePostTypeFilters.VIDEO)

@explore.get("/asks")
async def _asks(request):
    return await _handle_explore(request, "explore._asks", request.app.ctx.TumblrAPI.config.ExplorePostTypeFilters.ASKS)
