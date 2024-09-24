from .. import helpers

from . import collection_parsers, items

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
        if result := items.parse_item(post, post_index, total_raw_posts):
            posts.append(result)

    return posts, cursor
