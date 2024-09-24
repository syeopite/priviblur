from . import collection_parsers

def parse_timeline(initial_data):
    initial_data = initial_data["response"]
    return collection_parsers.TimelineParser.process(initial_data)


def parse_blog_timeline(initial_data):
    initial_data = initial_data["response"]
    return collection_parsers.BlogParser.process(initial_data)


def parse_post_list(initial_data):
    initial_data = initial_data["response"]
    return collection_parsers.process_post_list(initial_data)

