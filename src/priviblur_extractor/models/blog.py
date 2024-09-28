from typing import Sequence, Optional, NamedTuple

from . import base, timeline


class BlogTimeline(NamedTuple):
    """Object representing a blog page

    TODO better documentation
    """
    blog_info: timeline.Blog
    posts: Sequence[timeline.TimelinePost]
    total_posts: int | None
    next: Optional[base.Cursor] = None

    def to_json_serialisable(self):
        json_serializable = {
            "version": base.VERSION,
            "blog_info": self.blog_info.to_json_serialisable()
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
        json["blog_info"] = timeline.Blog.from_json(json["blog_info"])

        posts = []
        for post in json["posts"]:
            posts.append(timeline.TimelinePost.from_json(post))
        json["posts"] = posts

        if json["next"]:
            json["next"] = base.Cursor.from_json(json["next"])

        del json["version"]

        return cls(**json)
