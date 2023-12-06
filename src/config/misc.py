from typing import NamedTuple

class MiscellaneousConfig(NamedTuple):
    """NamedTuple that stores configuration values relating to Priviblur Extractor
    
    Attributes:
        main_response_timeout: Timeout for API requests to Tumblr
        image_response_timeout: Timeout for media requests to Tumblr
    """

    dev_mode: bool = False

