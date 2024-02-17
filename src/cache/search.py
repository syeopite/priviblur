import orjson

from .base import AccessCache
from .. import priviblur_extractor


class SearchCache(AccessCache):
    def __init__(self, ctx, query, continuation, **kwargs):
        self.ctx = ctx
        self.query = query
        self.continuation = continuation
        self.kwargs = kwargs

    @property
    def prefix(self):
        return "search"

    @property
    def cache_ttl(self):
        return self.ctx.PRIVIBLUR_CONFIG.cache.cache_feed_results_for

    async def fetch(self):
        """Fetches search results from Tumblr"""
        return await self.ctx.TumblrAPI.timeline_search(
            self.query,
            self.ctx.TumblrAPI.config.TimelineType.POST,
            continuation=self.continuation, 
            **self.kwargs
        )

    def parse(self, initial_results):
        return priviblur_extractor.parse_timeline(initial_results)

    def get_key(self):
        # search:<query>:<latest>:<post_filter>:<time_filter>:<continuation>
        path_to_cached_results = [self.query, ]

        if self.kwargs.get("latest") is True:
            path_to_cached_results.append("latest")
        if post_filter := self.kwargs.get("post_type_filter"):
            path_to_cached_results.append(post_filter.name.lower())
        if days := self.kwargs.get("days"):
            path_to_cached_results.append(days)

        base_key = f"{self.prefix}:{':'.join(path_to_cached_results)}"

        if self.continuation:
            full_key_with_continuation = f"{base_key}:{self.continuation}"
        else:
            full_key_with_continuation = base_key

        return base_key, full_key_with_continuation
    


async def get_search_results(ctx, query, continuation=None, **kwargs):
    search_cache = SearchCache(ctx, query, continuation, **kwargs)
    return await search_cache.get()