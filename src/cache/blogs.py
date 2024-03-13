import orjson

from .base import AccessCache
from .. import priviblur_extractor


class BlogPostsCache(AccessCache):
    def __init__(self, ctx, blog, continuation, **kwargs):
        super().__init__(
            ctx=ctx,
            prefix=f"blog:{blog}",
            cache_ttl=ctx.PRIVIBLUR_CONFIG.cache.cache_blog_feed_for,
            continuation=continuation,
            **kwargs
        )

        self.blog = blog

    async def fetch(self):
        """Fetches blog posts from Tumblr"""
        return await self.ctx.TumblrAPI.blog_posts(self.blog, continuation=self.continuation, **self.kwargs)

    def parse(self, initial_results):
        return priviblur_extractor.parse_blog_timeline(initial_results)

    def parse_cached_json(self, json):
        return priviblur_extractor.models.blog.Blog.from_json(json)

    def build_key(self):
        # blog:<blog_name>:<kwargs>
        path_to_cached_results = [self.prefix, ]
        for k,v in self.kwargs.items():
            if v:
                path_to_cached_results.append(f"{k}:{v}")

        return ':'.join(path_to_cached_results)


class BlogPostCache(AccessCache):
    def __init__(self, ctx, blog, post_id, **kwargs):
        super().__init__(
            ctx=ctx,
            prefix=f"blog:{blog}:post:{post_id}",
            cache_ttl=ctx.PRIVIBLUR_CONFIG.cache.cache_blog_post_for,
            **kwargs
        )

        self.blog = blog
        self.post_id = post_id

    async def fetch(self):
        return await self.ctx.TumblrAPI.blog_post(self.blog, self.post_id, **self.kwargs)

    def parse(self, initial_results):
        return priviblur_extractor.parse_timeline(initial_results)

    def build_key(self):
        # blog:<blog_name>:post:<post_id>:<kwargs>
        path_to_cached_results = [self.prefix, ]
        for k,v in self.kwargs.items():
            if v:
                path_to_cached_results.append(f"{k}:{v}")

        return ':'.join(path_to_cached_results)


class BlogSearchCache(AccessCache):
    def __init__(self, ctx, blog, query, page, **kwargs):
        super().__init__(
            ctx=ctx,
            prefix=f"blog:{blog}:search",
            cache_ttl=ctx.PRIVIBLUR_CONFIG.cache.cache_blog_feed_for,
            **kwargs
        )

        self.blog = blog
        self.query = query
        self.page = page

    async def fetch(self):
        return await self.ctx.TumblrAPI.blog_search(self.blog, self.query, page=self.page, **self.kwargs)

    def parse(self, initial_results):
        post_list, cursor = priviblur_extractor.parse_post_list(initial_results)
        # The cursor returned is basically None.
        return post_list

    def parse_cached_json(self, json):
        """Parses the cached JSON data into Priviblur objects"""
        posts = []
        for post in json["posts"]:
            posts.append(priviblur_extractor.models.timeline.TimelinePost.from_json(post))

        return posts

    def to_json(self, post_sequence):
        """Serializes a sequence of posts to JSON

        Additionally injects a version to bust cache"""
        posts = []
        for parsed_post in post_sequence:
            posts.append(parsed_post.to_json_serialisable())

        return orjson.dumps({"version": priviblur_extractor.models.VERSION, "posts": posts})

    def build_key(self):
        # blog:<blog_name>:<kwargs>:<page>
        path_to_cached_results = [self.prefix, self.query]
        for k,v in self.kwargs.items():
            if v:
                path_to_cached_results.append(f"{k}:{v}")

        if self.page:
            path_to_cached_results.append(f"page:{self.page}")

        return ':'.join(path_to_cached_results)


async def get_blog_posts(ctx, blog, continuation=None, **kwargs):
    blog_posts_cache = BlogPostsCache(ctx, blog, continuation, **kwargs)
    return await blog_posts_cache.get()


async def get_blog_search_results(ctx, blog, query, page=None, **kwargs):
    """Gets search results from a blog

    Returns a cached version when available, otherwise requests Tumblr.
    """
    blog_posts_cache = BlogSearchCache(ctx, blog, query, page, **kwargs)
    return await blog_posts_cache.get()


async def get_blog_post(ctx, blog, post_id, **kwargs):
    blog_post_cache = BlogPostCache(ctx, blog, post_id, **kwargs)
    return await blog_post_cache.get()
