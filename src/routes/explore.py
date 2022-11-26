import dominate
import sanic

import npf_renderer
import privblur_extractor

explore = sanic.Blueprint("explore", url_prefix="/explore")


async def render_content(results, url_handler):
    results = privblur_extractor.parse_container(results)

    doc = dominate.document(title="Trending topics")
    rendered = []
    for element in results.elements:
        tag = npf_renderer.format_npf(element.content, url_handler=url_handler)
        rendered.append(tag)

    for tag in rendered:
        doc.add(tag)
        doc.add(dominate.tags.hr())
        doc.add(dominate.tags.br())

    return doc


@explore.get("/")
async def _main(request):
    results = await request.app.ctx.TumblrAPI.explore_trending()
    doc = await render_content(results, request.app.ctx.URL_HANDLER)
    return sanic.response.html(doc.render(pretty=False))

@explore.get("/text")
async def _text(request):
    results = await request.app.ctx.TumblrAPI.explore_post(
        request.app.ctx.TumblrAPI.config.PostType.TEXT
    )
    doc = await render_content(results, request.app.ctx.URL_HANDLER)
    return sanic.response.html(doc.render(pretty=False))


@explore.get("/photos")
async def _photos(request):
    results = await request.app.ctx.TumblrAPI.explore_post(
        request.app.ctx.TumblrAPI.config.PostType.PHOTOS
    )
    doc = await render_content(results, request.app.ctx.URL_HANDLER)
    return sanic.response.html(doc.render(pretty=False))


@explore.get("/gifs")
async def _gifs(request):
    results = await request.app.ctx.TumblrAPI.explore_post(
        request.app.ctx.TumblrAPI.config.PostType.GIFS
    )
    doc = await render_content(results, request.app.ctx.URL_HANDLER)
    return sanic.response.html(doc.render(pretty=False))


