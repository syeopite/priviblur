import sanic

from npf_renderer.utils import BASIC_LAYOUT_CSS

assets = sanic.Blueprint("assets", url_prefix="/assets")

# Static assets
assets.static("/", "assets")


@assets.get("/css/base-post-layout.css")
async def base_post_layout(request):
    return sanic.response.text(BASIC_LAYOUT_CSS, content_type="text/css")


@assets.on_response
def add_assets_cache(request, response):
    response.headers["Cache-Control"] = "max-age=2629800, immutable"
