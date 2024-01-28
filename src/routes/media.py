import sanic

from ..helpers import exceptions

media = sanic.Blueprint("TumblrMedia", url_prefix="/tblr")


async def get_media(request, client, path_to_request):
    async with client.stream("GET", path_to_request) as tumblr_response:
        # Sanitize the headers given by Tumblr
        priviblur_response_headers = {}
        for header_key, header_value in tumblr_response.headers.items():
            if header_key.lower() not in request.app.ctx.BLACKLIST_RESPONSE_HEADERS:
                priviblur_response_headers[header_key] = header_value

        if tumblr_response.status_code == 301:
            if location := priviblur_response_headers.get("location"):
                location = request.app.ctx.URL_HANDLER(location)
                if not location.startswith("/"):
                    raise exceptions.TumblrInvalidRedirect()

                return sanic.redirect(location)
        elif tumblr_response.status_code == 429:
            return sanic.response.empty(status=502)

        priviblur_response = await request.respond(headers=priviblur_response_headers)

        async for chunk in tumblr_response.aiter_raw():
            await priviblur_response.send(chunk)


@media.get(r"/media/64/<path:path>")
async def _64_media(request: sanic.Request, path: str):
    """Proxies the requested media from 64.media.tumblr.com"""
    return await get_media(request, request.app.ctx.Media64Client, path)


@media.get(r"/media/49/<path:path>")
async def _49_media(request: sanic.Request, path: str):
    """Proxies the requested media from 49.media.tumblr.com"""
    return await get_media(request, request.app.ctx.Media49Client, path)


@media.get(r"/media/44/<path:path>")
async def _44_media(request: sanic.Request, path: str):
    """Proxies the requested media from 44.media.tumblr.com"""
    return await get_media(request, request.app.ctx.Media44Client, path)


@media.get(r"/assets/<path:path>")
async def _tb_assets(request: sanic.Request, path: str):
    """Proxies the requested media from assets.tumblr.com"""
    return await get_media(request, request.app.ctx.TumblrAssetClient, path)


@media.get(r"/static/<path:path>")
async def _tb_static(request: sanic.Request, path: str):
    """Proxies the requested media from static.tumblr.com"""
    return await get_media(request, request.app.ctx.TumblrStaticClient, path)
