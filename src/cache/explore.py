import orjson

from .base import AccessCache
from .. import priviblur_extractor


class ExploreCache(AccessCache):
    def __init__(self, ctx, type_, continuation, fetch_function, **kwargs):
        self.ctx = ctx
        self.type_ = type_
        self.continuation = continuation

        self.fetch_function = fetch_function
        self.kwargs = kwargs

    @property
    def prefix(self):
        return f"explore:{self.type_}"

    @property
    def cache_ttl(self):
        return self.ctx.PRIVIBLUR_CONFIG.cache.cache_feed_results_for

    async def fetch(self):
        """Fetches search results from Tumblr"""
        return await self.fetch_function(
            continuation=self.continuation,
            **self.kwargs
        )

    def parse(self, initial_results):
        return priviblur_extractor.parse_timeline(initial_results)

    def get_key(self):
        # explore:<type>:<continuation>
        base_key = self.prefix

        if self.continuation:
            full_key_with_continuation = f"{base_key}:{self.continuation}"
        else:
            full_key_with_continuation = base_key

        return base_key, full_key_with_continuation
    


async def get_explore_results(ctx, fetch_function, type_, continuation, **kwargs):
    search_cache = ExploreCache(ctx, type_, continuation, fetch_function, **kwargs)
    return await search_cache.get()