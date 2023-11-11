from typing import Optional, NamedTuple, Tuple


class Cursor(NamedTuple):
    """ Object representing Tumblr's API's "Next" object.

    Used to link to the next section of results. IE in search, explore, etc.
    """
    # method: str
    # href: str

    # Different from the cursor object
    cursor: str

    limit: Optional[int] = None  # How many posts to display per page?
    days: Optional[int] = None  # ?
    query: Optional[str] = None  # Query
    mode: Optional[str] = None  # Sorting
    timeline_type: Optional[str] = None  # Type of timeline object queried. Options are: "blog"s, "tag"s and "post"s.

    # Allows skipping certain results types like related blogs (or blog_search as it's called in API) and related_tags
    # Might be restricted to logined users only. Most investigations needed
    skip_components: Optional[str] = None

    reblog_info: Optional[bool] = None  # ?

    # fields {blogs: } TODO

    # Not always present
    post_type_filter: Optional[str] = None  # Type of filter selected. IE "Text" means text posts only.
