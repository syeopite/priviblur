from typing import Optional, NamedTuple, Tuple

# Used for cache busting
# Applied when .to_json_serialisable() is called
# Removed from serialized back with from_json()
VERSION = 5

class Cursor(NamedTuple):
    """ Object representing Tumblr's API's "Next" object.

    Used to link to the next section of results. IE in search, explore, etc.
    """
    # Different from the cursor object
    cursor: str

    limit: Optional[int] = None  # How many posts to display per page?
    days: Optional[int] = None   # Fetch posts published in the last N days
    query: Optional[str] = None  # Query
    mode: Optional[str] = None   # Sorting
    timeline_type: Optional[str] = None  # Type of timeline object queried. Options are: "blog"s, "tag"s and "post"s.

    # Allows skipping certain results types like related blogs (or blog_search as it's called in API) and related_tags
    skip_components: Optional[str] = None

    reblog_info: Optional[bool] = None

    # fields {blogs: } TODO

    # Not always present
    # Type of filter selected. IE "Text" means text posts only.
    post_type_filter: Optional[str] = None

    def to_json_serialisable(self):
        return self._asdict()

    @classmethod
    def from_json(cls, json):
        return cls(**json)
