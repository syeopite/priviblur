import orjson

from .base import AccessCache
from .. import priviblur_extractor


class TagBrowseCache(AccessCache):
    def __init__(self, ctx, tag, latest, continuation):
        self.ctx = ctx
        self.tag = tag
        self.latest = latest
        self.continuation = continuation

    @property
    def prefix(self):
        return "tagged"

    @property
    def cache_ttl(self):
        return self.ctx.PRIVIBLUR_CONFIG.cache.cache_feed_for

    async def fetch(self):
        """Fetches search results from Tumblr"""
        return await self.ctx.TumblrAPI.hubs_timeline(self.tag, latest=self.latest, continuation=self.continuation)

    def parse(self, initial_results):
        return priviblur_extractor.parse_timeline(initial_results)

    def get_key(self):
        # search:<query>:<latest>:<post_filter>:<time_filter>:<continuation>
        path_to_cached_results = [self.tag]

        if self.latest is True:
            path_to_cached_results.append("latest")

        base_key = f"{self.prefix}:{':'.join(path_to_cached_results)}"

        if self.continuation:
            full_key_with_continuation = f"{base_key}:{self.continuation}"
        else:
            full_key_with_continuation = base_key

        return base_key, full_key_with_continuation
    

async def get_tag_browse_results(ctx, tag, latest=False, continuation=None):
    tag_browse_cache = TagBrowseCache(ctx, tag, latest, continuation)
    return await tag_browse_cache.get()