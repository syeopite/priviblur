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

    def to_json_serialisable(self):
        json_serializable = self._asdict()

        if json_serializable["theme"]:
            json_serializable["theme"] = json_serializable["theme"].to_json_serialisable()

        return json_serializable

    @classmethod
    def from_json(cls, json):
        json["theme"] = misc.BlogTheme.from_json(json["theme"])
        return cls(**json)


class BrokenBlog(NamedTuple):
    name: str
    avatar: list[dict]

    def to_json_serialisable(self):
        return self._asdict()

    @classmethod
    def from_json(cls, json):
        return cls(**json)


class TimelinePostTrail(NamedTuple):
    id: str
    blog : Union[TimelineBlog, BrokenBlog]
    date: datetime.datetime
    content: Optional[list[dict]]
    layout: Optional[list[dict]]

    has_error : bool = False

    def to_json_serialisable(self):
        json_serializable = self._asdict()

        if json_serializable["blog"]:
            json_serializable["blog"] = json_serializable["blog"].to_json_serialisable()
        
        json_serializable["date"] = self.date.replace(tzinfo=datetime.timezone.utc).timestamp()

        return json_serializable

    @classmethod
    def from_json(cls, json):
        # Broken blogs contains only two attributes
        if len(json["blog"]) > 2:
            json["blog"] = TimelineBlog.from_json(json["blog"])
        else:
            json["blog"] = BrokenBlog.from_json(json["blog"])

        json["date"] = datetime.datetime.utcfromtimestamp(json["date"])

        return cls(**json)


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
    trail: List[TimelinePostTrail]

    note_count: Optional[int] = None
    like_count: Optional[int] = None
    reblog_count: Optional[int] = None
    reply_count: Optional[int] = None

    reblog_from: Optional[misc.ReblogAttribution] = None
    reblog_root: Optional[misc.ReblogAttribution] = None

    community_labels: list[CommunityLabel] = []

    def to_json_serialisable(self):
        json_serializable = self._asdict()

        json_serializable["date"] = self.date.replace(tzinfo=datetime.timezone.utc).timestamp()
        json_serializable["trail"] = [trail.to_json_serialisable() for trail in  self.trail]

        # Serialize the attributes that are NamedTuples to JSON
        for key in ("blog", "reblog_from", "reblog_root"):
            if json_serializable[key]:
                json_serializable[key] = json_serializable[key].to_json_serialisable()

        return json_serializable

    @classmethod
    def from_json(cls, json):
        json["date"] = datetime.datetime.utcfromtimestamp(json["date"])

        trails = []
        for trail in json["trail"]:
            trails.append(TimelinePostTrail.from_json(trail))
        json["trail"] = trails

        for key, object_ in (("blog", TimelineBlog), ("reblog_from", misc.ReblogAttribution), ("reblog_root", misc.ReblogAttribution)):
            if json[key]:
                json[key] = object_.from_json(json[key])

        community_labels = []
        for label_value in json["community_labels"]:
            community_labels.append(CommunityLabel(label_value))
        json["community_labels"] = community_labels

        return cls(**json)


TimelineObjects = Union[TimelineBlog, TimelinePost]


class Timeline(NamedTuple):
    """Object representing Tumblr API's Timeline object.

    Refers to data on a certain page. IE Search or explore
    """
    elements: List[TimelineObjects | None]
    next: Optional[base.Cursor] = None

    def to_json_serialisable(self):
        elements = []
        for element in self.elements:
            if isinstance(element, TimelineBlog):
                elements.append({"blog": element.to_json_serialisable()})
            else:
                elements.append({"post": element.to_json_serialisable()})

        next_ = self.next
        if next_:
            next_ = next_.to_json_serialisable()

        return {
            "version": base.VERSION,
            "elements": elements,
            "next": next_
        }

    @classmethod
    def from_json(cls, json):
        elements = []
        for element in json["elements"]:
            if blog := element.get("blog"):
                elements.append(TimelineBlog.from_json(blog))
            else:
                elements.append(TimelinePost.from_json(element["post"]))

        json["elements"] = elements

        if json["next"]:
            json["next"] = base.Cursor.from_json(json["next"])

        del json["version"]

        return cls(**json)
