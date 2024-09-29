from typing import Sequence, Optional, NamedTuple

from . import base, timeline


class BlogTimeline(NamedTuple):
    """Object representing a blog page

    TODO better documentation
    """
    blog_info: timeline.Blog
    posts: Sequence[timeline.Post]
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
            posts.append(timeline.Post.from_json(post))
        json["posts"] = posts

        if json["next"]:
            json["next"] = base.Cursor.from_json(json["next"])

        del json["version"]

        return cls(**json)


class Timeline(NamedTuple):
    """Object representing Tumblr API's Timeline object.

    Refers to data on a certain page. IE Search or explore
    """
    elements: Sequence[timeline.Post | timeline.Blog]
    next: Optional[base.Cursor] = None

    def to_json_serialisable(self):
        elements = []
        for element in self.elements:
            if isinstance(element, timeline.Blog):
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
                elements.append(timeline.Blog.from_json(blog))
            else:
                elements.append(timeline.Post.from_json(element["post"]))

        json["elements"] = elements

        if json["next"]:
            json["next"] = base.Cursor.from_json(json["next"])

        del json["version"]

        return cls(**json)
