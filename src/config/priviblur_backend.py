from typing import NamedTuple


class PriviblurBackendConfig(NamedTuple):
    """NamedTuple that stores configuration values relating to Priviblur Extractor

    Attributes:
        main_response_timeout: Timeout for API requests to Tumblr
        image_response_timeout: Timeout for media requests to Tumblr
    """

    main_response_timeout: int = 10
    image_response_timeout: int = 30
