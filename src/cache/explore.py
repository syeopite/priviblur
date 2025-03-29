import orjson

from .base import AccessCache
from .. import priviblur_extractor


class ExploreCache(AccessCache):
    def __init__(self, ctx, type_, continuation, fetch_function, **kwargs):
        super().__init__(
            ctx=ctx,
            prefix=f"explore:{type_}",
            cache_ttl=ctx.PRIVIBLUR_CONFIG.cache.cache_feed_for,
            continuation=continuation,
            **kwargs,
        )

        self.fetch_function = fetch_function

    async def fetch(self):
        """Fetches search results from Tumblr"""
        return await self.fetch_function(continuation=self.continuation, **self.kwargs)

    def parse(self, initial_results):
        return priviblur_extractor.parse_timeline(initial_results)

    def build_key(self):
        return self.prefix


async def get_explore_results(ctx, fetch_function, type_, continuation, **kwargs):
    search_cache = ExploreCache(ctx, type_, continuation, fetch_function, **kwargs)
    return await search_cache.get()
