from .. import helpers

from .parsers import _TimelineParser, _BlogParser, _CursorParser, _TimelinePostParser, parse_item

logger = helpers.LOGGER.getChild("parse")

def parse_timeline(initial_data):
    initial_data = initial_data["response"]
    return _TimelineParser.process(initial_data)


def parse_blog_timeline(initial_data):
    initial_data = initial_data["response"]
    return _BlogParser.process(initial_data)


def parse_post_list(initial_data):
    initial_data = initial_data["response"]

    cursor = _CursorParser.process(initial_data)

    # Now the posts contained within
    posts = []
    total_raw_posts = len(initial_data["posts"])
    for post_index, post in enumerate(initial_data["posts"]):
        if result := parse_item(post, post_index, total_raw_posts, use_parsers=[_TimelinePostParser]):
            posts.append(result)

    return posts, cursor
