import sanic
import aiohttp

from src.exceptions import exceptions

media = sanic.Blueprint("TumblrMedia", url_prefix="/tblr")


async def get_media(
    request, client: aiohttp.ClientSession, path_to_request, additional_headers=None, base_url=""
):
    async with client.get(
        f"{base_url}/{path_to_request}", headers=additional_headers
    ) as tumblr_response:
        # Sanitize the headers given by Tumblr
        priviblur_response_headers = {}
        for header_key, header_value in tumblr_response.headers.items():
            if header_key.lower() not in request.app.ctx.BLACKLIST_RESPONSE_HEADERS:
                priviblur_response_headers[header_key] = header_value

        if tumblr_response.status == 301:
            if location := priviblur_response_headers.get("location"):
                location = request.app.ctx.URL_HANDLER(location)
                if not location.startswith("/"):
                    raise exceptions.TumblrInvalidRedirect()

                return sanic.redirect(location)
        elif tumblr_response.status == 429:
            return sanic.response.empty(status=502)

        priviblur_response = await request.respond(headers=priviblur_response_headers)

        async for chunk in tumblr_response.content.iter_any():
            await priviblur_response.send(chunk)

    await priviblur_response.eof()


@media.get("/media/<cdn:str>/<path:path>")
async def _media_cdn(request: sanic.Request, cdn: str, path: str):
    """Proxies media from *.media.tumblr.com"""
    match cdn:
        case "64":
            return await get_media(request, request.app.ctx.Media64Client, path)
        case "49":
            return await get_media(request, request.app.ctx.Media49Client, path)
        case "44":
            return await get_media(request, request.app.ctx.Media44Client, path)
        case "ve":
            return await get_media(
                request,
                request.app.ctx.MediaVeClient,
                path,
                additional_headers={
                    "accept": "video/webm,video/ogg,video/*;q=0.9, application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5"
                },
            )
        case "va":
            return await get_media(
                request,
                request.app.ctx.MediaVaClient,
                path,
                additional_headers={
                    "accept": "video/webm,video/ogg,video/*;q=0.9, application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5"
                },
            )
        case _:
            return await get_media(
                request,
                request.app.ctx.MediaGenericClient,
                path,
                base_url=f"https://{cdn}.media.tumblr.com",
            )


@media.get(r"/a/<path:path>")
async def _a_media(request: sanic.Request, path: str):
    """Proxies the requested media from va.media.tumblr.com"""
    additional_headers = {
        "accept": "audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5"
    }
    return await get_media(
        request, request.app.ctx.AudioClient, path, additional_headers=additional_headers
    )


@media.get(r"/assets/<path:path>")
async def _tb_assets(request: sanic.Request, path: str):
    """Proxies the requested media from assets.tumblr.com"""
    return await get_media(request, request.app.ctx.TumblrAssetClient, path)


@media.get(r"/static/<path:path>")
async def _tb_static(request: sanic.Request, path: str):
    """Proxies the requested media from static.tumblr.com"""
    return await get_media(request, request.app.ctx.TumblrStaticClient, path)
