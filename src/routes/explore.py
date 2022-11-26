import dominate
import sanic
import sanic_ext

import npf_renderer
import privblur_extractor

explore = sanic.Blueprint("explore", url_prefix="/explore")


async def render_results(initial_results, url_handler):
        timeline = privblur_extractor.parse_container(initial_results)

        return await sanic_ext.render(
            "explore.jinja",
            context={
                "url_handler": url_handler,
                "timeline": timeline,
                "format_npf": npf_renderer.format_npf
            }
        )


@explore.get("/")
async def _main(request):
    initial_results = await request.app.ctx.TumblrAPI.explore_trending()
    return await render_results(initial_results, request.app.ctx.URL_HANDLER)


@explore.get("/text")
async def _text(request):
    initial_results = await request.app.ctx.TumblrAPI.explore_post(
        request.app.ctx.TumblrAPI.config.PostType.TEXT
    )
    return await render_results(initial_results, request.app.ctx.URL_HANDLER)



@explore.get("/photos")
async def _photos(request):
    initial_results = await request.app.ctx.TumblrAPI.explore_post(
        request.app.ctx.TumblrAPI.config.PostType.PHOTOS
    )
    return await render_results(initial_results, request.app.ctx.URL_HANDLER)



@explore.get("/gifs")
async def _gifs(request):
    initial_results = await request.app.ctx.TumblrAPI.explore_post(
        request.app.ctx.TumblrAPI.config.PostType.GIFS
    )
    return await render_results(initial_results, request.app.ctx.URL_HANDLER)



