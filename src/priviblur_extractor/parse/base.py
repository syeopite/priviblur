from . import collection_parsers

def parse_timeline(initial_data):
    return collection_parsers.TimelineParser.process(initial_data["response"])


def parse_blog_timeline(initial_data):
    return collection_parsers.BlogTimelineParser.process(initial_data["response"])


def parse_post_list(initial_data):
    return collection_parsers.process_post_list(initial_data["response"])

