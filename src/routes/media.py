import sanic

media = sanic.Blueprint("TumblrMedia", url_prefix="/tblr")


async def get_media(request, client_to_use, path_to_request):
    async with client_to_use.get(f"/{path_to_request}") as tumblr_img_resp:
        privblur_response_headers = {}
        for header_key, header_value in tumblr_img_resp.headers.items():
            if header_key.lower() not in request.app.ctx.BLACKLIST_RESPONSE_HEADERS:
                privblur_response_headers[header_key] = header_value

        privblur_img_resp = await request.respond(headers=privblur_response_headers)

        async for chunk in tumblr_img_resp.content.iter_any():
            await privblur_img_resp.send(chunk)


@media.get(r"/media/64/<path:path>")
async def _64_media(request: sanic.Request, path: str):
    """Proxies the requested media from 64.media.tumblr.com"""
    return await get_media(request, request.app.ctx.Media64Client, path)


@media.get(r"/media/49/<path:path>")
async def _49_media(request: sanic.Request, path: str):
    """Proxies the requested media from 49.media.tumblr.com"""
    return await get_media(request, request.app.ctx.Media49Client, path)


@media.get(r"/assets/<path:path>")
async def _tb_assets(request: sanic.Request, path: str):
    """Proxies the requested media from assets.tumblr.com"""
    return await get_media(request, request.app.ctx.TumblrAssetClient, path)


