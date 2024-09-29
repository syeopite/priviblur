import datetime
import enum
from typing import Union, NamedTuple, List, Optional, Union

from . import misc


# Avatars = namedtuple("avatars", "")


class Blog(NamedTuple):
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


class PostTrail(NamedTuple):
    id: Optional[str]
    blog : Union[Blog, BrokenBlog]
    date: Optional[datetime.datetime]
    content: Optional[list[dict]]
    layout: Optional[list[dict]]

    def to_json_serialisable(self):
        json_serializable = self._asdict()

        if json_serializable["blog"]:
            json_serializable["blog"] = json_serializable["blog"].to_json_serialisable()

        if json_serializable["date"]:
            json_serializable["date"] = self.date.replace(tzinfo=datetime.timezone.utc).timestamp()

        return json_serializable

    @classmethod
    def from_json(cls, json):
        # Broken blogs contains only two attributes
        if len(json["blog"]) > 2:
            json["blog"] = Blog.from_json(json["blog"])
        else:
            json["blog"] = BrokenBlog.from_json(json["blog"])

        if json["date"] is not None:
            json["date"] = datetime.datetime.utcfromtimestamp(json["date"])

        return cls(**json)


class CommunityLabel(enum.Enum):
    MATURE = 0  # Generic catch all
    DRUG_USE = 1
    VIOLENCE = 2
    SEXUAL_THEMES = 3


class Post(NamedTuple):
    blog: Blog

    id: str
    post_url: str
    slug: str
    date: Optional[datetime.datetime]
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
    trail: List[PostTrail]

    note_count: Optional[int] = None
    like_count: Optional[int] = None
    reblog_count: Optional[int] = None
    reply_count: Optional[int] = None

    reblog_from: Optional[misc.ReblogAttribution] = None
    reblog_root: Optional[misc.ReblogAttribution] = None

    community_labels: list[CommunityLabel] = []

    def to_json_serialisable(self):
        json_serializable = self._asdict()

        if json_serializable["date"]:
            json_serializable["date"] = self.date.replace(tzinfo=datetime.timezone.utc).timestamp()
        json_serializable["trail"] = [trail.to_json_serialisable() for trail in  self.trail]

        # Serialize the attributes that are NamedTuples to JSON
        for key in ("blog", "reblog_from", "reblog_root"):
            if json_serializable[key]:
                json_serializable[key] = json_serializable[key].to_json_serialisable()

        return json_serializable

    @classmethod
    def from_json(cls, json):
        if json["date"] is not None:
            json["date"] = datetime.datetime.utcfromtimestamp(json["date"])

        trails = []
        for trail in json["trail"]:
            trails.append(PostTrail.from_json(trail))
        json["trail"] = trails

        for key, object_ in (("blog", Blog), ("reblog_from", misc.ReblogAttribution), ("reblog_root", misc.ReblogAttribution)):
            if json[key]:
                json[key] = object_.from_json(json[key])

        community_labels = []
        for label_value in json["community_labels"]:
            community_labels.append(CommunityLabel(label_value))
        json["community_labels"] = community_labels

        return cls(**json)

