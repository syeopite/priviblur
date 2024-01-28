import urllib.parse

import sanic
from ..helpers import exceptions

miscellaneous = sanic.Blueprint("miscellaneous", url_prefix="/")

@miscellaneous.get(r"/at/<path:path>")
async def _at_links(request: sanic.Request, path : str):
    """Redirects for at.tumblr.com links"""
    response = await request.app.ctx.TumblrAtClient.head(path)
    if response.status_code == 301:
        location = urllib.parse.urlparse(response.headers["location"])
        if location.path.startswith("/"):
            return sanic.redirect(location.path)

    raise exceptions.TumblrInvalidRedirect()