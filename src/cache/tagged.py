from .base import AccessCache
from .. import priviblur_extractor


class TagBrowseCache(AccessCache):
    def __init__(self, ctx, tag, latest, continuation, **kwargs):
        super().__init__(
            ctx=ctx,
            prefix=f"tagged",
            cache_ttl=ctx.PRIVIBLUR_CONFIG.cache.cache_feed_for,
            continuation=continuation,
            **kwargs,
        )

        self.tag = tag
        self.latest = latest

    async def fetch(self):
        """Fetches posts from Tumblr with the given tag"""
        return await self.ctx.TumblrAPI.hubs_timeline(
            self.tag, latest=self.latest, continuation=self.continuation
        )

    def parse(self, initial_results):
        return priviblur_extractor.parse_timeline(initial_results)

    def build_key(self):
        # tagged:<tag>:<latest>:<continuation>
        path_to_cached_results = [self.prefix, self.tag]

        if self.latest is True:
            path_to_cached_results.append("latest")

        return ":".join(path_to_cached_results)


async def get_tag_browse_results(ctx, tag, latest=False, continuation=None):
    tag_browse_cache = TagBrowseCache(ctx, tag, latest, continuation)
    return await tag_browse_cache.get()
