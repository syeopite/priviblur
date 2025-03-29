from . import collection_parsers


def parse_timeline(initial_data):
    return collection_parsers.TimelineParser.process(initial_data["response"])


def parse_blog_timeline(initial_data, is_search=False):
    if is_search:
        return collection_parsers.BlogTimelineParser(
            initial_data["response"]
        ).parse_blog_search_timeline()
    else:
        return collection_parsers.BlogTimelineParser.process(initial_data["response"])


def parse_note_timeline(initial_data):
    """Parses a note timeline object"""
    return collection_parsers.NoteTimelineParser.process(initial_data["response"])
