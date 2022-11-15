import sanic

media = sanic.Blueprint("media", url_prefix="/media")


@media.get(r"/image/<path:path>")
async def _64_media(request: sanic.Request, path: str):
    """Proxies the requested media from 64.media.tumblr.com"""
    async with request.app.ctx.ImageClient.get(f"/{path}") as tumblr_img_resp:
        privblur_response_headers = {}
        for header_key, header_value in tumblr_img_resp.headers.items():
            if header_key.lower() not in request.app.ctx.BLACKLIST_RESPONSE_HEADERS:
                privblur_response_headers[header_key] = header_value

        privblur_img_resp = await request.respond(headers=privblur_response_headers)

        async for chunk in tumblr_img_resp.content.iter_any():
            await privblur_img_resp.send(chunk)
