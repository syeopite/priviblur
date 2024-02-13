import orjson

async def get_poll_results(ctx, blog, post_id,poll_id, expired=False):
    """Gets poll results from the given data
    
    Attempts to retrieve from the cache first and foremost, and only requests when the data is either unavailable or expired.
    """
    if ctx.CacheDb:
        cached_result = await ctx.CacheDb.hgetall(f"polls:{poll_id}")
        if cached_result:
            timestamp = cached_result.pop("timestamp")
            poll_results = {k:int(v) for k, v in cached_result.items()}

            return {"timestamp": timestamp, "results": poll_results}
        else:
            initial_results = await _fetch_poll_results(ctx.TumblrAPI, blog, post_id, poll_id)
            await _cache_poll_results(ctx, initial_results, poll_id, expired)

            return initial_results
    else:
        return await _fetch_poll_results(ctx.TumblrAPI, blog, post_id, poll_id)


async def _fetch_poll_results(tumblr_api, blog, post_id, poll_id):
    """Requests Tumblr for poll results"""
    initial_results = await tumblr_api.poll_results(blog, post_id, poll_id)
    return initial_results["response"]


async def _cache_poll_results(ctx, results, poll_id, expired):
    """Caches the given poll results"""
    if expired:
        ttl = ctx.PRIVIBLUR_CONFIG.cache.cache_expired_poll_results_for
    else:
        ttl = ctx.PRIVIBLUR_CONFIG.cache.cache_active_poll_results_for

    pipeline = ctx.CacheDb.pipeline()

    cache_id = f"polls:{poll_id}"

    pipeline.hset(cache_id, mapping={
        **results["results"],
        "timestamp": results["timestamp"],
    })

    pipeline.expire(cache_id, ttl)
    
    await pipeline.execute()

    