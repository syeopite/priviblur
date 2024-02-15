import orjson

from .. import priviblur_extractor


async def get_search_results(ctx, query, continuation=None, **kwargs):
    if ctx.CacheDb:
        # search:<query>:<latest>:<post_filter>:<time_filter>:<continuation>
        key = [query, ]

        if kwargs.get("latest") is True:
            key.append("latest")
        if post_filter := kwargs.get("post_type_filter"):
            key.append(post_filter.name.lower())
        if days := kwargs.get("days"):
            key.append(days)

        key = f"search:{':'.join(key)}"

        if continuation:
            full_key = f"{key}:{continuation}"
        else:
            full_key = key 

        cached_result = await ctx.CacheDb.get(full_key)

        # See comment in _handle_fetched_search_results as to why "0"
        if not cached_result or cached_result == "0":
            initial_results = await _fetch_search_results(ctx, query, continuation, **kwargs)

            # If we did not already allocate a slot for the current search with continuation
            # then we do not cache it.
            if continuation and not cached_result:
                timeline = priviblur_extractor.parse_timeline(initial_results)
            else:
                timeline = await _handle_fetched_search_results(ctx, key, continuation, initial_results)

            return timeline
        else:
            initial_results = orjson.loads(cached_result)
            return priviblur_extractor.parse_timeline(initial_results)
    else:
        initial_results = await _fetch_search_results(ctx, query, continuation, **kwargs)
        return priviblur_extractor.parse_timeline(initial_results)


async def _fetch_search_results(ctx, query, continuation, **kwargs):
    """Requests Tumblr for search results with the given queries"""
    return await ctx.TumblrAPI.timeline_search(query, ctx.TumblrAPI.config.TimelineType.POST, continuation=continuation, **kwargs)


async def _handle_fetched_search_results(ctx, key, continuation, results):
    """Caches the given search results and returns a parsed Timeline object"""
    pipeline = ctx.CacheDb.pipeline()

    if continuation:
        full_key = f"{key}:{continuation}"
    else:
        full_key = key 

    pipeline.set(full_key, orjson.dumps(results))
    pipeline.expire(key, ctx.PRIVIBLUR_CONFIG.cache.cache_feed_results_for)

    # Allocate key slot for the next continuation
    #
    # When a given continuation is invalid Tumblr returns the data for the initial page. As such,
    # we need to add in an extra check here to ensure that a malicious user does not arbitrarily add
    # in data to the cache
    # 
    # "0" is used as a placeholder 
    timeline = priviblur_extractor.parse_timeline(results)
    if timeline.next and timeline.next.cursor:
        next_key = f"{key}:{timeline.next.cursor}"
        pipeline.setnx(next_key, "0")
        pipeline.expire(next_key, ctx.PRIVIBLUR_CONFIG.cache.cache_feed_results_for)
    
    await pipeline.execute()

    return timeline

