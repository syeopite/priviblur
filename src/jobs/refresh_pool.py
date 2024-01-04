import asyncio
import functools

import orjson

from .. import priviblur_extractor

async def refresh_pool(app, origin, create_image_client):
    """Refreshes the connection pool identified by `origin`"""
    match origin:
        case "Priviblur.TumblrMedia._64_media":
            app.ctx.Media64Client = create_image_client("https://64.media.tumblr.com")
        case "Priviblur.TumblrMedia._49_media":
            app.ctx.Media49Client = create_image_client("https://49.media.tumblr.com")
        case "Priviblur.TumblrMedia._44_media":
            app.ctx.Media44Client = create_image_client("https://44.media.tumblr.com")
        case "Priviblur.TumblrMedia._tb_assets":
            app.ctx.TumblrAssetClient = create_image_client("https://assets.tumblr.com")
        case "Priviblur.TumblrMedia._tb_static":
            app.ctx.TumblrStaticClient = create_image_client("https://static.tumblr.com")
        case _:
            app.ctx.TumblrAPI = await priviblur_extractor.TumblrAPI.create(
                app.ctx.PRIVIBLUR_CONFIG.backend.main_request_timeout,
                json_loads=orjson.loads,
                post_success_function=functools.partial(app.ctx.PoolTimeoutTracker.increment, "main")
            )

async def refresh_pool_task(app, create_image_client):
    """Detects and refreshes poisoned connection pool"""
    amount_of_pools_refreshed = 0

    try:
        while True:
            for origin, count in app.ctx.PoolTimeoutTracker.counter.items():
                # If a pool only has a 70% success rate then we'll refresh the pool
                if round(count["success"]/count["total"], 2) < 0.70:
                    app.ctx.LOGGER.info("Refreshing connection pool for \"{origin}\"")
                    await refresh_pool(app, origin, create_image_client)
                    amount_of_pools_refreshed += 1

            app.ctx.LOGGER.info(f"Finished pool refresh task. Refreshed {amount_of_pools_refreshed} pools")
            # The counter is reset here as to ensure we don't get a success rate so high that failures won't
            # be able to budge the success rate
            app.ctx.PoolTimeoutTracker.counter = {}
            await asyncio.sleep(900)
    except asyncio.exceptions.CancelledError:
        pass
