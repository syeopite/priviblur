import abc
import typing

import orjson

from .. import priviblur_extractor


class AccessCache(abc.ABC):
    def __init__(self, ctx, prefix, cache_ttl, continuation=None, **kwargs):
        self.ctx = ctx
        self.prefix = prefix
        self.cache_ttl = cache_ttl

        self.continuation = continuation
        self.kwargs = kwargs

    @abc.abstractmethod
    def fetch(self) -> typing.Dict[str, typing.Any]:
        """Fetches results from Tumblr"""
        pass

    @abc.abstractmethod
    def parse(self, initial_results):
        """Parses the initial JSON response from Tumblr"""
        pass

    @abc.abstractmethod
    def build_key(self) -> str:
        """Creates a key to get/store an item within the cache"""
        pass

    def parse_cached_json(self, json):
        return priviblur_extractor.models.timelines.Timeline.from_json(json)

    def to_json(self, parsed_results):
        return orjson.dumps(parsed_results.to_json_serialisable())

    def get_key(self):
        base_key = self.build_key()

        if self.continuation:
            full_key_with_continuation = f"{base_key}:{self.continuation}"
        else:
            full_key_with_continuation = base_key

        return base_key, full_key_with_continuation

    def allocate_slot_for_continuation(self, base_key, pipeline, timeline):
        if hasattr(timeline, "next") and timeline.next and timeline.next.cursor:
            next_key = f"{base_key}:{timeline.next.cursor}"
            pipeline.setnx(next_key, "0")
            pipeline.expire(next_key, self.cache_ttl)

            self.ctx.LOGGER.debug(
                'Cache: Allocating a slot for continuation batch with key "%s"', next_key
            )

    async def parse_and_cache(self, base_key, full_key_with_continuation, initial_results):
        """Inserts the given results into the cache within the given key

        Creates a placeholder item within the cache for the next continuation batch if applicable
        """
        pipeline = self.ctx.CacheDb.pipeline()
        timeline = self.parse(initial_results)

        pipeline.set(full_key_with_continuation, self.to_json(timeline))
        pipeline.expire(full_key_with_continuation, self.cache_ttl)

        # Allocate key slot for the next continuation
        #
        # When a given continuation is invalid Tumblr returns the data for the initial page. As such,
        # we need to add in an extra check here to ensure that a malicious user does not arbitrarily add
        # in data to the cache
        #
        # "0" is used as a placeholder

        self.allocate_slot_for_continuation(base_key, pipeline, timeline)

        await pipeline.execute()

        return timeline

    async def get_cached(self):
        """Retrieves an item from the cache

        Fetches new data and inserts into the cache when it is unable to do so
        """
        base_key, full_key_with_continuation = self.get_key()
        cached_result = await self.ctx.CacheDb.get(full_key_with_continuation)

        # See comment in self.parse_and_cache as to why "0"
        if not cached_result or cached_result == "0":
            initial_results = await self.fetch()

            # When the current request has a continuation token attached, we'll only cache
            # when a slot has already been allocated for it from the previous request.
            if self.continuation and not cached_result:
                return self.parse(initial_results)
            else:
                self.ctx.LOGGER.info('Cache: Adding "%s" to the cache', full_key_with_continuation)
                return await self.parse_and_cache(
                    base_key, full_key_with_continuation, initial_results
                )
        else:
            self.ctx.LOGGER.info('Cache: Cached version of "%s" found', full_key_with_continuation)

            initial_results_from_cache = orjson.loads(cached_result)

            if initial_results_from_cache["version"] != priviblur_extractor.models.VERSION:
                self.ctx.LOGGER.debug(
                    "Cache: Version mismatch! Cached object is from a different version of Priviblur (%(cached_version)s != %(priviblur_version)s). Fetching new response...",
                    dict(
                        cached_version=initial_results_from_cache["version"],
                        priviblur_version=priviblur_extractor.models.VERSION,
                    ),
                )
                new_initial_results = await self.fetch()
                return await self.parse_and_cache(
                    base_key, full_key_with_continuation, new_initial_results
                )

            return self.parse_cached_json(initial_results_from_cache)

    async def get(self):
        """Retrieves some data from either the cache or Tumblr itself"""
        if self.ctx.CacheDb:
            return await self.get_cached()
        else:
            initial_results = await self.fetch()
            return self.parse(initial_results)
