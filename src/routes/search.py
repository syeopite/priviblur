import urllib.parse

import dominate
import sanic

import npf_renderer
import privblur_extractor

search = sanic.Blueprint("search", url_prefix="/search")


async def render_content(results, url_handler):
    results = privblur_extractor.parse_container(results)

    doc = dominate.document(title="Trending topics")
    rendered = []
    for element in results.elements:
        tag = npf_renderer.format_npf(element.content, url_handler=url_handler, layouts=element.layout)
        rendered.append(tag)

    for tag in rendered:
        doc.add(tag)
        doc.add(dominate.tags.hr())
        doc.add(dominate.tags.br())

    return doc


@search.get("/<query:str>")
async def _main(request: sanic.Request, query: str):
    query = urllib.parse.unquote(query)
    timeline_type = request.app.ctx.TumblrAPI.config.TimelineType

    results = await request.app.ctx.TumblrAPI.timeline_search(query, timeline_type.POST)

    doc = await render_content(results, request.app.ctx.URL_HANDLER)
    return sanic.response.html(doc.render(pretty=False))
