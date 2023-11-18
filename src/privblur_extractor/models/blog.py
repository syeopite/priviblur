from typing import Sequence, Optional, NamedTuple

from . import base, timeline

class Blog(NamedTuple):
    """Object representing a blog page

    TODO better documentation
    """
    blog_info: timeline.TimelineBlog
    posts: Sequence[timeline.TimelinePost | None]
    total_posts: int | None
    next: Optional[base.Cursor] = None


