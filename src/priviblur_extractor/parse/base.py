from .. import helpers

from . import collection_parsers

from .items import PostParser, parse_item

logger = helpers.LOGGER.getChild("parse")

def parse_timeline(initial_data):
    initial_data = initial_data["response"]
    return collection_parsers.TimelineParser.process(initial_data)


def parse_blog_timeline(initial_data):
    initial_data = initial_data["response"]
    return collection_parsers.BlogParser.process(initial_data)


def parse_post_list(initial_data):
    initial_data = initial_data["response"]

    cursor = collection_parsers.CursorParser.process(initial_data)

    # Now the posts contained within
    posts = []
    total_raw_posts = len(initial_data["posts"])
    for post_index, post in enumerate(initial_data["posts"]):
        if result := parse_item(post, post_index, total_raw_posts, use_parsers=[PostParser]):
            posts.append(result)

    return posts, cursor
