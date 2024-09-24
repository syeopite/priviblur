"""Creates models that represents "packages" of Tumblr objects

Eg a regular timeline, or posts on a blog.

"""

from .. import helpers, models
from .parsers import BlogInfoParser, PostParser, parse_item

logger = helpers.LOGGER.getChild("parse")

class CursorParser:
    def __init__(self, raw_cursor) -> None:
        self.target = raw_cursor

    @classmethod
    def process(cls, initial_data):
        if target := helpers.dig_dict(initial_data, ("links", "next")):
            return cls(target["queryParams"]).parse()
        else:
            return None

    def parse(self):
        return models.base.Cursor(
            cursor=self.target.get("cursor") or self.target.get("pageNumber"),
            limit=self.target.get("days"),
            days=self.target.get("query"),
            query=self.target.get("mode"),
            mode=self.target.get("timelineType"),
            skip_components=self.target.get("skipComponent"),
            reblog_info=self.target.get("reblogInfo"),
            post_type_filter=self.target.get("postTypeFilter")
        )


class TimelineParser:
    """Parses Tumblr's API response into a Timeline object"""
    def __init__(self, target) -> None:
        self.target = target

    @classmethod
    def process(cls, initial_data):
        if target := initial_data.get("timeline"):
            logger.debug("TimelineParser: Parser found! Beginning parsing...")
            return cls(target).parse()
        else:
            return None

    def parse(self):
        # First let's begin with the cursor object
        cursor = CursorParser.process(self.target)

        # Now the elements contained within
        elements = []
        total_raw_elements = len(self.target["elements"])
        for element_index, element in enumerate(self.target["elements"]):
            if result := parse_item(element, element_index, total_raw_elements, [
                PostParser
            ]):
                elements.append(result)

        return models.timeline.Timeline(
            elements=elements,
            next = cursor,
        )


class BlogParser:
    """Parses Tumblr's API response into a Blog object"""
    def __init__(self, target) -> None:
        self.target = target

    @classmethod
    def process(cls, initial_data):
        if initial_data.get("blog"):
            logger.debug("BlogParser: Parser found! Beginning parsing...")
            return cls(initial_data).parse()
        else:
            return None

    def parse(self):
        # First let's begin with the cursor object
        cursor = CursorParser.process(self.target)

        # Then the blog info
        blog = BlogInfoParser.process(self.target["blog"], force_parse=True)

        # Now the posts contained within
        posts = []
        total_raw_posts = len(self.target["posts"])
        for post_index, post in enumerate(self.target["posts"]):
            if result := parse_item(post, post_index, total_raw_posts, [PostParser]):
                posts.append(result)

        return models.blog.Blog(
            blog_info=blog,
            posts=posts,
            total_posts = self.target.get("totalPosts"),
            next = cursor,
        )