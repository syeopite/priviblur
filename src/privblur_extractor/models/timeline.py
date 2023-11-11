import datetime
from typing import Union, NamedTuple, List, Optional

from . import base


# Avatars = namedtuple("avatars", "")


class TimelineBlog(NamedTuple):
    name: str
    # [{"width": 512, "height": 512, url: "..."}, {"width": ...}...]
    avatar: list[dict]
    title: str
    url: str
    is_adult: bool

    # If Neue Post Format this is the result:
    #  [
    #      {"type": "text", "text": "...",
    #       "formatting": [
    #           {"start": 0, "end": 10, type:"link", url: ""},
    #           {"start": 15, "end":40, type: "bold"} # More research needed!
    #           ],
    #
    #       }
    #  ]
    # Else it'd just be pure HTML. TODO add support in the parser
    #
    description_npf: list[dict]

    uuid: str
    is_paywall_on: bool


class TimelinePost(NamedTuple):
    blog: TimelineBlog

    id: str
    post_url: str
    slug: str  # A custom URL slug to use in the post's permalink URL
    date: datetime.datetime
    # state: str  # TODO Enum as in published or not. Kinda useless for us.
    # reblog_key: str
    tags: list[str]
    summary: str

    can_like: bool
    can_reblog: bool
    can_reply: bool
    display_avatar: bool
    # intractability: str TODO

    is_advertisement: bool
    is_nsfw: bool

    content: Optional[list[dict]]
    layout: Optional[list[dict]]
    trail: Optional[list[dict]]

    note_count: Optional[int] = None
    like_count: Optional[int] = None
    reblog_count: Optional[int] = None
    reply_count: Optional[int] = None


TimelineObjects = Union[TimelineBlog]


class Timeline(NamedTuple):
    """Object representing Tumblr API's Timeline object.

    Refers to data on a certain page. IE Search or explore
    """
    elements: List[TimelineObjects | None]
    next: Optional[base.Cursor] = None