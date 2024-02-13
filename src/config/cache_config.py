from typing import NamedTuple, Optional

class CacheConfig(NamedTuple):
    """NamedTuple that stores configuration values relating to the redis cache
    
    Attributes:
        url: to connect to the redis instance
        cache_active_poll_results_for: Amount of seconds to cache poll results from active polls
        cache_expired_poll_results_for: Amount of seconds to cache poll results from expired polls
    """

    url: Optional[str] = None

    cache_active_poll_results_for: int = 3600
    cache_expired_poll_results_for: int = 86400
