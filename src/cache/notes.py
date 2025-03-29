from .base import AccessCache
from .. import priviblur_extractor


class NotesTimelineCache(AccessCache):
    def __init__(self, ctx, blog, post_id, type_, fetch_function, **kwargs):
        super().__init__(
            ctx=ctx,
            prefix=f"blog:{blog}:post:{post_id}:notes:{type_}",
            cache_ttl=ctx.PRIVIBLUR_CONFIG.cache.cache_feed_for,
            continuation=kwargs.get("after_id") or kwargs.get("before_timestamp") or None,
            **kwargs,
        )

        self.blog = blog
        self.post_id = post_id

        self.type_ = type_
        self.fetch_function = fetch_function

    async def fetch(self):
        """Fetches search results from Tumblr"""
        return await self.fetch_function(self.blog, self.post_id, **self.kwargs)

    def parse(self, initial_results):
        return priviblur_extractor.parse_note_timeline(initial_results)

    def parse_cached_json(self, json):
        return priviblur_extractor.models.timelines.NoteTimeline.from_json(json)

    def allocate_slot_for_continuation(self, base_key, pipeline, timeline):
        if timeline.before_timestamp:
            next_key = f"{base_key}:{timeline.before_timestamp}"
        elif timeline.after_id:
            next_key = f"{base_key}:{timeline.after_id}"
        else:
            return

        pipeline.setnx(next_key, "0")
        pipeline.expire(next_key, self.cache_ttl)
        self.ctx.LOGGER.debug(
            f'Cache: Allocating a slot for next "%s" notes batch with key "%s"',
            self.type_,
            next_key,
        )

    def build_key(self):
        # blog:<blog_name>:post:<post_id>:<kwargs>
        path_to_cached_results = [self.prefix]

        if mode := self.kwargs.get("mode"):
            path_to_cached_results.append(mode.name.lower())

        elif "return_likes" in self.kwargs:
            path_to_cached_results.append("reblogs_only")

        if self.kwargs.get("latest"):
            path_to_cached_results.append("latest")

        return f"{':'.join(path_to_cached_results)}"


async def get_post_notes(ctx, blog: str, post_id: str, type_: str, fetch_function, **kwargs):
    return await NotesTimelineCache(ctx, blog, post_id, type_, fetch_function, **kwargs).get()
