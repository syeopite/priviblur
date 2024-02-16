import datetime
import enum
from typing import Union, NamedTuple, List, Tuple, Optional, Union

from . import base, misc


# Avatars = namedtuple("avatars", "")


class TimelineBlog(NamedTuple):
    name: str
    # [{"width": 512, "height": 512, url: "..."}, {"width": ...}...]
    avatar: list[dict]
    title: str
    url: str
    is_adult: bool

    description_npf: list[dict]
    uuid: str
    theme: misc.BlogTheme
    is_paywall_on: bool

    # If blog is deactivated or not
    active: bool = False


class BrokenBlog(NamedTuple):
    name: str
    avatar: list[dict]


class TimelinePostTrail(NamedTuple):
    blog : Union[TimelineBlog]
    content: Optional[list[dict]]
    layout: Optional[list[dict]]

    has_error : bool = False


class CommunityLabel(enum.Enum):
    MATURE = 0  # Generic catch all
    DRUG_USE = 1
    VIOLENCE = 2
    SEXUAL_THEMES = 3


class TimelinePost(NamedTuple):
    blog: TimelineBlog

    id: str
    post_url: str
    slug: str
    date: datetime.datetime
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
    trail: Optional[TimelinePostTrail]

    note_count: Optional[int] = None
    like_count: Optional[int] = None
    reblog_count: Optional[int] = None
    reply_count: Optional[int] = None

    reblog_from: Optional[misc.ReblogAttribution] = None
    reblog_root: Optional[misc.ReblogAttribution] = None

    community_labels: list[CommunityLabel] = []


TimelineObjects = Union[TimelineBlog]


class Timeline(NamedTuple):
    """Object representing Tumblr API's Timeline object.

    Refers to data on a certain page. IE Search or explore
    """
    elements: List[TimelineObjects | None]
    next: Optional[base.Cursor] = None
