"""Creates models that represents "packages" of Tumblr objects

Eg a regular timeline, or posts on a blog.

"""

from . import items
from .. import helpers, models

logger = helpers.LOGGER.getChild("parse")

class _CursorParser:
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
            return cls(target).parse()
        else:
            return None

    def parse(self):
        # First let's begin with the cursor object
        cursor = _CursorParser.process(self.target)

        # Now the elements contained within
        elements = []
        total_raw_elements = len(self.target["elements"])
        for element_index, element in enumerate(self.target["elements"]):
            if result := items.parse_item(
                    element,
                    element_index,
                    total_raw_elements,
                    use_parsers=(items.PostParser, items.SignpostParser)
                ):
                elements.append(result)

        return models.timelines.Timeline(
            elements=elements,
            next = cursor,
        )


class BlogTimelineParser:
    """Parses Tumblr's API response into a Blog object"""
    def __init__(self, target) -> None:
        self.target = target

    @classmethod
    def process(cls, initial_data):
        if "blog" in initial_data:
            return cls(initial_data).parse()
        else:
            return None

    def parse(self):
        # First let's begin with the cursor object
        cursor = _CursorParser.process(self.target)

        # Then the blog info
        blog = items.BlogParser(self.target["blog"]).parse()

        # Now the posts contained within
        posts = []
        total_raw_posts = len(self.target["posts"])
        for post_index, post in enumerate(self.target["posts"]):
            if result := items.parse_item(post, post_index, total_raw_posts):
                posts.append(result)

        return models.timelines.BlogTimeline(
            blog_info=blog,
            posts=posts,
            total_posts = self.target.get("totalPosts"),
            next = cursor,
        )

    def parse_blog_search_timeline(self):
        cursor = _CursorParser.process(self.target)

        # Now the posts contained within
        posts = []
        total_raw_posts = len(self.target["posts"])
        for post_index, post in enumerate(self.target["posts"]):
            if result := items.parse_item(post, post_index, total_raw_posts):
                posts.append(result)

        return models.timelines.BlogTimeline(
            blog_info=posts[0].blog,
            posts=posts,
            total_posts = total_raw_posts,
            next = cursor,
        )


class NoteTimelineParser:
    """Parses a sequence of various note types"""
    def __init__(self, target) -> None:
        self.target = target

    @classmethod
    def process(cls, initial_data):
        if "timeline" in initial_data:
            return cls(initial_data).parse()
        elif "notes" in initial_data:
            return cls(initial_data).parse_note_sequence()
        else:
            return None

    def parse(self):
        timeline = self.target["timeline"]

        total_raw_notes = len(timeline["elements"])

        notes = []
        for index, note in enumerate(timeline["elements"]):
            notes.append(
                items.parse_item(
                    note,
                    index,
                    total_raw_notes,
                    use_parsers=(items.ReplyNoteParser, items.ReblogNoteParser)
                )
            )

        query_for_next_batch =  helpers.dig_dict(timeline, ("links", "next", "queryParams"))

        if query_for_next_batch:
            before_timestamp = query_for_next_batch.get("beforeTimestamp")
            after_id = query_for_next_batch.get("after")
        else:
            before_timestamp = None
            after_id = None

        return self.return_note_model(
            notes,
            before_timestamp=before_timestamp,
            after_id=after_id
        )

    def parse_note_sequence(self):
        """Parses a sequence of notes

        An alternative structure sometimes returned by Tumblr.
        This is used for pure reblog notes (no tags or content) and likes."""

        sequence = self.target["notes"]
        total_raw_notes = len(sequence)

        notes = []
        for index, note in enumerate(sequence):
            result = items.parse_item(
                    note,
                    index,
                    total_raw_notes,
                    use_parsers=(items.LikeNoteParser, items.ReblogNoteParser)
                )

            notes.append(result)

        before_timestamp = helpers.dig_dict(self.target, ("links", "next", "queryParams", "beforeTimestamp"))

        return self.return_note_model(notes, before_timestamp=before_timestamp)


    def return_note_model(self, notes, before_timestamp = None, after_id = None):
        return models.timelines.NoteTimeline(
            notes = notes,
            total_notes=self.target["totalNotes"],
            total_likes=self.target["totalLikes"],
            total_reblogs=self.target["totalReblogs"],
            total_replies=self.target["totalReplies"],

            before_timestamp=before_timestamp,
            after_id=after_id
        )
