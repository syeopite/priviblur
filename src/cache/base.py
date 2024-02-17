import abc
import typing

import orjson

class AccessCache(abc.ABC):
    @abc.abstractmethod
    def get_key(self) -> typing.Tuple[str, str]:
        """Creates a key to get/store an item within the cache"""
        pass

    @abc.abstractmethod
    def fetch(self) -> typing.Dict[str, typing.Any]:
        """Fetches results from Tumblr"""
        pass

    @abc.abstractmethod
    def parse(self, initial_results):
        """Parses the initial JSON response from Tumblr"""
        pass

    @property
    @abc.abstractmethod
    def prefix(self) -> str:
        """The first segment of the key to get/store an item within the cache"""
        pass

    @property
    @abc.abstractmethod
    def cache_ttl(self) -> int:
        """How long the keep the item within the cache"""
        pass

    async def parse_and_cache(self, base_key, full_key_with_continuation, initial_results):
        """Inserts the given results into the cache within the given key
        
        Creates a placeholder item within the cache for the next continuation batch if applicable"""
        pipeline = self.ctx.CacheDb.pipeline()

        pipeline.set(full_key_with_continuation, orjson.dumps(initial_results))
        pipeline.expire(full_key_with_continuation, self.cache_ttl)

        # Allocate key slot for the next continuation
        #
        # When a given continuation is invalid Tumblr returns the data for the initial page. As such,
        # we need to add in an extra check here to ensure that a malicious user does not arbitrarily add
        # in data to the cache
        # 
        # "0" is used as a placeholder 
        timeline = self.parse(initial_results)
        if timeline.next and timeline.next.cursor:
            next_key = f"{base_key}:{timeline.next.cursor}"
            pipeline.setnx(next_key, "0")
            pipeline.expire(next_key, self.cache_ttl)
        
        await pipeline.execute()

        return timeline

    async def get_cached(self):
        """Retrieves an item from the cache
        
        Fetches new data and inserts into the cache when it is unable to do so"""
        base_key, full_key_with_continuation = self.get_key()

        cached_result = await self.ctx.CacheDb.get(full_key_with_continuation)
        # See comment in self.cache_and_prepare as to why "0"
        if not cached_result or cached_result == "0":
            initial_results = await self.fetch()

            # If we did not already allocate a slot for the current search with continuation
            # then we do not cache it.
            if self.continuation and not cached_result:
                return self.parse(initial_results)
            else:
                return await self.parse_and_cache(base_key, full_key_with_continuation, initial_results)
        else:
            initial_results = orjson.loads(cached_result)
            return self.parse(initial_results)

    async def get(self):
        if self.ctx.CacheDb:
            return await self.get_cached()
        else:
            initial_results = await self.fetch()
            return self.parse(initial_results)
