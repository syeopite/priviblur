import sanic
import dominate
import privblur_extractor
import npf_renderer


explore = sanic.Blueprint("explore", url_prefix="/explore")


@explore.get("/")
async def _main(request):
    results = await request.app.ctx.TumblrAPI.explore_trending()
    results = privblur_extractor.parse_container(results)

    doc = dominate.document(title="Trending topics")
    rendered = []
    for element in results.elements:
        tag = npf_renderer.format_npf(element.content)
        rendered.append(tag)

    for tag in rendered:
        doc.add(tag)
        doc.add(dominate.tags.hr())
        doc.add(dominate.tags.br())

    return sanic.response.html(doc.render(pretty=False))



