from typing import NamedTuple, Optional

class CacheConfig(NamedTuple):
    """NamedTuple that stores configuration values relating to the redis cache
    
    Attributes:
        url: to connect to the redis instance
    """

    url: Optional[str] = None
