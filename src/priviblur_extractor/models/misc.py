from typing import Optional, NamedTuple, Tuple

class ReblogAttribution(NamedTuple):
    """Object representing reblog author information from individual posts"""
    post_id: str
    post_url: str
    blog_name: str
    blog_title: str

class HeaderInfo(NamedTuple):
    header_image: str
    focused_header_image: str
    scaled_header_image: str

class BlogTheme(NamedTuple):
    avatar_shape: str
    background_color: str
    body_font: str
    header_info : HeaderInfo