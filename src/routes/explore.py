import html
import urllib.parse

import sanic
import sanic_ext

import npf_renderer

from .. import privblur_extractor

explore = sanic.Blueprint("explore", url_prefix="/explore")


async def render_results(app, endpoint, initial_results, url_handler):
        timeline = privblur_extractor.parse_container(initial_results)

        return await sanic_ext.render(
            "explore.jinja",
            context={
                "app": app,
                "endpoint": endpoint,
                "html_escape": html.escape,
                "url_escape": urllib.parse.quote,
                "url_handler": url_handler,
                "timeline": timeline,
                "format_npf": npf_renderer.format_npf
            }
        )


@explore.get("/")
async def _main(request):
    return sanic.redirect(request.app.url_for("explore._trending"))  # /explore/trending


@explore.get("/trending")
async def _trending(request):
    if continuation := request.args.get("continuation"):
        continuation = urllib.parse.unquote(continuation)

    initial_results = await request.app.ctx.TumblrAPI.explore_trending(continuation=continuation)
    return await render_results(request.app, request.app.url_for("explore._trending"),
                                initial_results, request.app.ctx.URL_HANDLER)


@explore.get("/text")
async def _text(request):
    if continuation := request.args.get("continuation"):
        continuation = urllib.parse.unquote(continuation)

    initial_results = await request.app.ctx.TumblrAPI.explore_post(
        request.app.ctx.TumblrAPI.config.PostType.TEXT, continuation=continuation
    )
    return await render_results(request.app, request.app.url_for("explore._text"),
                                initial_results, request.app.ctx.URL_HANDLER)


@explore.get("/photos")
async def _photos(request):
    if continuation := request.args.get("continuation"):
        continuation = urllib.parse.unquote(continuation)

    initial_results = await request.app.ctx.TumblrAPI.explore_post(
        request.app.ctx.TumblrAPI.config.PostType.PHOTOS, continuation=continuation
    )
    return await render_results(request.app, request.app.url_for("explore._photos"),
                                initial_results, request.app.ctx.URL_HANDLER)


@explore.get("/gifs")
async def _gifs(request):
    if continuation := request.args.get("continuation"):
        continuation = urllib.parse.unquote(continuation)

    initial_results = await request.app.ctx.TumblrAPI.explore_post(
        request.app.ctx.TumblrAPI.config.PostType.GIFS, continuation=continuation
    )
    return await render_results(request.app, request.app.url_for("explore._gifs"),
                                initial_results, request.app.ctx.URL_HANDLER)


@explore.get("/quotes")
async def _quotes(request):
    if continuation := request.args.get("continuation"):
        continuation = urllib.parse.unquote(continuation)

    initial_results = await request.app.ctx.TumblrAPI.explore_post(
        request.app.ctx.TumblrAPI.config.PostType.QUOTES, continuation=continuation
    )
    return await render_results(request.app, request.app.url_for("explore._quotes"),
                                initial_results, request.app.ctx.URL_HANDLER)


@explore.get("/chats")
async def _chats(request):
    if continuation := request.args.get("continuation"):
        continuation = urllib.parse.unquote(continuation)

    initial_results = await request.app.ctx.TumblrAPI.explore_post(
        request.app.ctx.TumblrAPI.config.PostType.CHATS, continuation=continuation
    )
    return await render_results(request.app, request.app.url_for("explore._chats"),
                                initial_results, request.app.ctx.URL_HANDLER)


@explore.get("/asks")
async def _asks(request):
    if continuation := request.args.get("continuation"):
        continuation = urllib.parse.unquote(continuation)

    initial_results = await request.app.ctx.TumblrAPI.explore_post(
        request.app.ctx.TumblrAPI.config.PostType.ASKS, continuation=continuation
    )
    return await render_results(request.app, request.app.url_for("explore._asks"),
                                initial_results, request.app.ctx.URL_HANDLER)

