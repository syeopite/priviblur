import json
from typing import Sequence, Optional, NamedTuple

from . import base
from .post import Post, ReplyNote, ReblogNote, LikeNote
from .misc import Signpost
from .blog import Blog


class BlogTimeline(NamedTuple):
    """Object representing a blog page

    TODO better documentation
    """

    blog_info: Blog
    posts: Sequence[Post]
    total_posts: int | None
    next: Optional[base.Cursor] = None

    def to_json_serialisable(self):
        json_serializable = {
            "version": base.VERSION,
            "blog_info": self.blog_info.to_json_serialisable(),
        }
        json_serializable["posts"] = [post.to_json_serialisable() for post in self.posts]
        json_serializable["total_posts"] = self.total_posts

        if self.next:
            json_serializable["next"] = self.next.to_json_serialisable()
        else:
            json_serializable["next"] = None

        return json_serializable

    @classmethod
    def from_json(cls, json):
        json["blog_info"] = Blog.from_json(json["blog_info"])

        posts = []
        for post in json["posts"]:
            posts.append(Post.from_json(post))
        json["posts"] = posts

        if json["next"]:
            json["next"] = base.Cursor.from_json(json["next"])

        del json["version"]

        return cls(**json)


class NoteTimeline(NamedTuple):
    notes: Sequence[ReplyNote | ReblogNote | LikeNote]

    total_notes: int
    total_replies: int
    total_reblogs: int
    total_likes: int

    # Used to fetch next batch of post notes
    #
    # Reblogs and likes both use before_timestamp
    # but replies uses after_id
    before_timestamp: Optional[str] = None
    after_id: Optional[str] = None

    def to_json_serialisable(self):
        json_serializable = self._asdict()

        json_serializable["version"] = base.VERSION

        json_serializable["notes"] = [note.to_json_serialisable() for note in self.notes]

        return json_serializable

    @classmethod
    def from_json(cls, json):
        notes = []
        for note in json["notes"]:
            match note["type"]:
                case "reply":
                    notes.append(ReplyNote.from_json(note))
                case "reblog":
                    notes.append(ReblogNote.from_json(note))
                case "like":
                    notes.append(LikeNote.from_json(note))

        json["notes"] = notes

        del json["version"]

        return cls(**json)


class Timeline(NamedTuple):
    """Object representing Tumblr API's Timeline object.

    Refers to data on a certain page. IE Search or explore
    """

    elements: Sequence[Post | Blog]
    signposts: Sequence[Signpost] = []
    next: Optional[base.Cursor] = None

    def to_json_serialisable(self):
        elements = []
        for element in self.elements:
            if isinstance(element, Post):
                elements.append({"post": element.to_json_serialisable()})
            else:
                elements.append({"blog": element.to_json_serialisable()})

        signposts = []
        for signpost in self.signposts:
            signposts.append(signpost.to_json_serialisable())

        next_ = self.next
        if next_:
            next_ = next_.to_json_serialisable()

        return {
            "version": base.VERSION,
            "elements": elements,
            "signposts": signposts,
            "next": next_,
        }

    @classmethod
    def from_json(cls, json):
        elements = []
        for element in json["elements"]:
            if post := element.get("post"):
                elements.append(Post.from_json(post))
            else:
                elements.append(Blog.from_json(element.get("blog")))

        json["elements"] = elements

        signposts = []
        for signpost in json["signposts"]:
            signposts.append(Signpost.from_json(signpost))

        if json["next"]:
            json["next"] = base.Cursor.from_json(json["next"])

        del json["version"]

        return cls(**json)
