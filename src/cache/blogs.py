import orjson

from .base import AccessCache
from .. import priviblur_extractor


class BlogPostsCache(AccessCache):
    def __init__(self, ctx, blog, continuation, **kwargs):
        self.ctx = ctx
        self.blog = blog
        self.continuation = continuation
        self.kwargs = kwargs

    @property
    def prefix(self):
        return f"blog:{self.blog}"

    @property
    def cache_ttl(self):
        return self.ctx.PRIVIBLUR_CONFIG.cache.cache_blog_feed_for

    async def fetch(self):
        """Fetches blog posts from Tumblr"""
        return await self.ctx.TumblrAPI.blog_posts(self.blog, continuation=self.continuation, **self.kwargs)

    def parse(self, initial_results):
        return priviblur_extractor.parse_blog_timeline(initial_results)

    def get_key(self):
        # blog:<blog_name>:<kwargs>:<continuation>
        path_to_cached_results = [self.prefix, ]
        for k,v in self.kwargs.items():
            if v:
                path_to_cached_results.append(f"{k}:{v}")

        base_key = ':'.join(path_to_cached_results)

        if self.continuation:
            full_key_with_continuation = f"{base_key}:{self.continuation}"
        else:
            full_key_with_continuation = base_key

        return base_key, full_key_with_continuation


class BlogPostCache(AccessCache):
    def __init__(self, ctx, blog, post_id, **kwargs):
        self.ctx = ctx
        self.blog = blog
        self.post_id = post_id

        self.kwargs = kwargs

        self.continuation = None

    @property
    def prefix(self):
        return f"blog:{self.blog}:post:{self.post_id}"

    @property
    def cache_ttl(self):
        return self.ctx.PRIVIBLUR_CONFIG.cache.cache_blog_post_for

    async def fetch(self):
        return await self.ctx.TumblrAPI.blog_post(self.blog, self.post_id, **self.kwargs)

    def parse(self, initial_results):
        return priviblur_extractor.parse_timeline(initial_results)

    def get_key(self):
        # blog:<blog_name>:post:<post_id>:<kwargs>
        path_to_cached_results = [self.prefix, ]
        for k,v in self.kwargs.items():
            if v:
                path_to_cached_results.append(f"{k}:{v}")

        base_key = ':'.join(path_to_cached_results)

        return base_key, base_key


async def get_blog_posts(ctx, blog, continuation=None, **kwargs):
    blog_posts_cache = BlogPostsCache(ctx, blog, continuation, **kwargs)
    return await blog_posts_cache.get()


async def get_blog_post(ctx, blog, post_id, **kwargs):
    blog_post_cache = BlogPostCache(ctx, blog, post_id, **kwargs)
    return await blog_post_cache.get()
