import datetime
import enum

from typing import Optional, Union, NamedTuple, Sequence

from . import blog


class CommunityLabel(enum.Enum):
    MATURE = 0  # Generic catch all
    DRUG_USE = 1
    VIOLENCE = 2
    SEXUAL_THEMES = 3


class ReplyNote(NamedTuple):
    uuid: str
    reply_id: str
    date: Optional[datetime.datetime]

    content: Optional[Sequence[dict]]
    layout: Optional[Sequence[dict]]

    blog: blog.Blog

    def to_json_serialisable(self):
        json_serializable = self._asdict()

        json_serializable["type"] = "reply"

        json_serializable["blog"] = json_serializable["blog"].to_json_serialisable()
        if self.date:
            json_serializable["date"] = self.date.replace(tzinfo=datetime.timezone.utc).timestamp()

        return json_serializable

    @classmethod
    def from_json(cls, json):
        if json["date"] is not None:
            json["date"] = datetime.datetime.fromtimestamp(json["date"], tz=datetime.timezone.utc)

        if json["blog"]:
            json["blog"] = blog.Blog.from_json(json["blog"])

        del json["type"]

        return cls(**json)


class ReblogNote(NamedTuple):
    uuid: str
    id: str

    blog: blog.Blog

    content: Optional[Sequence[dict]]
    layout: Optional[Sequence[dict]]
    tags: Sequence[str]

    reblogged_from: str

    date: Optional[datetime.datetime]

    community_labels: Sequence[CommunityLabel]

    def to_json_serialisable(self):
        json_serializable = self._asdict()

        json_serializable["type"] = "reblog"

        json_serializable["blog"] = json_serializable["blog"].to_json_serialisable()
        if self.date:
            json_serializable["date"] = self.date.replace(tzinfo=datetime.timezone.utc).timestamp()

        return json_serializable

    @classmethod
    def from_json(cls, json):
        if json["date"] is not None:
            json["date"] = datetime.datetime.utcfromtimestamp(json["date"])

        if json["blog"]:
            json["blog"] = blog.Blog.from_json(json["blog"])

        community_labels = []
        for label_value in json["community_labels"]:
            community_labels.append(CommunityLabel(label_value))

        json["community_labels"] = community_labels

        del json["type"]

        return cls(**json)


class LikeNote(NamedTuple):
    blog_name: str
    blog_uuid: str
    blog_title: str
    date: Optional[datetime.datetime]

    avatar: list[dict]

    # TODO
    # avatar_shape

    def to_json_serialisable(self):
        json_serializable = self._asdict()

        json_serializable["type"] = "like"

        if self.date:
            json_serializable["date"] = self.date.replace(tzinfo=datetime.timezone.utc).timestamp()

        return json_serializable

    @classmethod
    def from_json(cls, json):
        if json["date"] is not None:
            json["date"] = datetime.datetime.fromtimestamp(json["date"], tz=datetime.timezone.utc)

        del json["type"]

        return cls(**json)


class ReblogAttribution(NamedTuple):
    """Object representing reblog author information from individual posts"""
    post_id: str
    post_url: str
    blog_name: str
    blog_title: str

    def to_json_serialisable(self):
        return self._asdict()

    @classmethod
    def from_json(cls, json):
        return cls(**json)


class PostTrail(NamedTuple):
    id: Optional[str]
    blog : Union[blog.Blog, blog.BrokenBlog]
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
            json["blog"] = blog.Blog.from_json(json["blog"])
        else:
            json["blog"] = blog.BrokenBlog.from_json(json["blog"])

        if json["date"] is not None:
            json["date"] = datetime.datetime.utcfromtimestamp(json["date"])

        return cls(**json)


class Post(NamedTuple):
    blog: blog.Blog

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
    trail: Sequence[PostTrail]

    note_count: Optional[int] = None
    like_count: Optional[int] = None
    reblog_count: Optional[int] = None
    reply_count: Optional[int] = None

    reblog_from: Optional[ReblogAttribution] = None
    reblog_root: Optional[ReblogAttribution] = None

    community_labels: list[CommunityLabel] = []

    def to_json_serialisable(self):
        json_serializable = self._asdict()

        if json_serializable["date"]:
            json_serializable["date"] = self.date.replace(tzinfo=datetime.timezone.utc).timestamp()
        json_serializable["trail"] = [trail.to_json_serialisable() for trail in self.trail]

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

        for key, object_ in (("blog", blog.Blog), ("reblog_from", ReblogAttribution), ("reblog_root", ReblogAttribution)):
            if json[key]:
                json[key] = object_.from_json(json[key])

        community_labels = []
        for label_value in json["community_labels"]:
            community_labels.append(CommunityLabel(label_value))
        json["community_labels"] = community_labels

        return cls(**json)
