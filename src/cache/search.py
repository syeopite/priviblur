import orjson

from .base import AccessCache
from .. import priviblur_extractor


class SearchCache(AccessCache):
    def __init__(self, ctx, query, continuation, **kwargs):
        super().__init__(
            ctx=ctx,
            prefix=f"search",
            cache_ttl=ctx.PRIVIBLUR_CONFIG.cache.cache_feed_for,
            continuation=continuation,
            **kwargs,
        )

        self.query = query

    async def fetch(self):
        """Fetches search results from Tumblr"""
        return await self.ctx.TumblrAPI.timeline_search(
            self.query,
            self.ctx.TumblrAPI.config.TimelineType.POST,
            continuation=self.continuation,
            **self.kwargs,
        )

    def parse(self, initial_results):
        return priviblur_extractor.parse_timeline(initial_results)

    def build_key(self):
        # search:<query>:<latest>:<post_filter>:<time_filter>:<continuation>
        path_to_cached_results = [
            self.query,
        ]

        if self.kwargs.get("latest") is True:
            path_to_cached_results.append("latest")

        if post_filter := self.kwargs.get("post_type_filter"):
            path_to_cached_results.append(post_filter.name.lower())

        if days := self.kwargs.get("days"):
            path_to_cached_results.append(days)

        return f"{self.prefix}:{':'.join(path_to_cached_results)}"


async def get_search_results(ctx, query, continuation=None, **kwargs):
    search_cache = SearchCache(ctx, query, continuation, **kwargs)
    return await search_cache.get()
