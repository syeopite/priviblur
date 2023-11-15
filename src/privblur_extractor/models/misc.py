from typing import Optional, NamedTuple, Tuple

class ReblogAttribution(NamedTuple):
    """Object representing reblog author information from individual posts"""
    post_id: str
    post_url: str
    blog_name: str
    blog_title: str

