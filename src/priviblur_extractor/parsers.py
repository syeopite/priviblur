import datetime

from . import helpers, models

logger = helpers.LOGGER.getChild("parse")


class _CursorParser:
    @staticmethod
    def process(initial_data):
        if target := helpers.dig_dict(initial_data, ("links", "next")):
            return _CursorParser.__parse(target)
        else:
            return None

    @staticmethod
    def __parse(target):
        target = target["queryParams"]
        return models.base.Cursor(
            cursor=target.get("cursor") or target.get("pageNumber"),
            limit=target.get("days"),
            days=target.get("query"),
            query=target.get("mode"),
            mode=target.get("timelineType"),
            skip_components=target.get("skipComponent"),
            reblog_info=target.get("reblogInfo"),
            post_type_filter=target.get("postTypeFilter")
        )


class _TimelineParser:
    """Parses Tumblr's API response into a Timeline object"""

    @staticmethod
    def process(initial_data):
        if target := initial_data.get("timeline"):
            logger.debug("_TimelineParser: Parser found! Beginning parsing...")
            return _TimelineParser.__parse(target)
        else:
            return None

    @staticmethod
    def __parse(target):
        # First let's begin with the cursor object
        cursor = _CursorParser.process(target)

        # Now the elements contained within
        elements = []
        total_raw_elements = len(target["elements"])
        for element_index, element in enumerate(target["elements"]):
            if result := parse_item(element, element_index, total_raw_elements):
                elements.append(result)

        return models.timeline.Timeline(
            elements=elements,
            next = cursor,
        )


class _BlogParser:
    """Parses Tumblr's API response into a Blog object"""
    @staticmethod
    def process(initial_data):
        if initial_data.get("blog"):
            logger.debug("_BlogParser: Parser found! Beginning parsing...")
            return _BlogParser.__parse(initial_data)
        else:
            return None

    @staticmethod
    def __parse(target):
        # First let's begin with the cursor object
        cursor = _CursorParser.process(target)

        # Then the blog info
        blog = _TimelineBlogParser.process(target["blog"], force_parse=True)

        # Now the posts contained within
        posts = []
        total_raw_posts = len(target["posts"])
        for post_index, post in enumerate(target["posts"]):
            if result := parse_item(post, post_index, total_raw_posts):
                posts.append(result)

        return models.blog.Blog(
            blog_info=blog,
            posts=posts,
            total_posts = target.get("totalPosts"),
            next = cursor,
        )


class _BlogThemeParser:
    @staticmethod
    def process(initial_data):
        if theme := initial_data.get("theme"):
            logger.debug("_BlogThemeParser: Parser found! Beginning parsing...")
            return _BlogThemeParser.__parse(theme)
        else:
            return None

    @staticmethod
    def __parse(target):
        # TODO more theme data
        header_info = models.misc.HeaderInfo(
            target["headerImage"],
            target["headerImageFocused"],
            target["headerImageScaled"],
        )

        return models.misc.BlogTheme(
            avatar_shape = target["avatarShape"],
            background_color = target["backgroundColor"],
            body_font = target["bodyFont"],
            header_info=header_info
        )

class _TimelineBlogParser:
    @staticmethod
    def process(initial_data, force_parse=False):
        if initial_data.get("objectType") == "blog":
            return _TimelineBlogParser.__parse(initial_data["resources"][0])
        elif force_parse:
            # Assume packaged as {"blog": <blog data>}
            return _TimelineBlogParser.__parse(initial_data)
        else:
            return None

    @staticmethod
    def __parse(target):
        theme = _BlogThemeParser.process(target)

        return models.timeline.TimelineBlog(
            name=target["name"],
            avatar=target["avatar"],
            title=target["title"],
            url=target["url"],
            is_adult=target["isAdult"],
            description_npf=target["descriptionNpf"],
            uuid=target["uuid"],
            theme=theme,
            is_paywall_on=target["isPaywallOn"]
        )


class _TimelinePostParser:
    @staticmethod
    def process(initial_data):
        if initial_data.get("objectType") == "post":
            logger.debug("_TimelinePostParser: Parser found! Beginning parsing...")
            return _TimelinePostParser.__parse(initial_data)
        else:
            return None

    @staticmethod
    def __parse(target):
        blog = _TimelineBlogParser.process(target["blog"], force_parse=True)

        assert blog is not None

        id = target["id"]

        note_count = target.get("noteCount")
        like_count = None
        reblog_count = None
        reply_count = None

        if can_like := target["canReply"]:
            reply_count = target["replyCount"]
        if can_reblog := target["canReblog"]:
            reblog_count = target["reblogCount"]
        if can_reply := target["canLike"]:
            like_count = target["likeCount"]

        # We check multiple keys as a precautionary measure.
        if target.get("advertiserId") or target.get("adId") or target.get("adProviderId"):
            is_advertisement = True
        else:
            is_advertisement = False

        content = target["content"]
        layout = target["layout"]
        trail = target["trail"]

        trails = []
        for trail_post in trail:
            try:
                trail_blog = _TimelineBlogParser.process(trail_post["blog"], force_parse=True)
                trail_content = trail_post["content"]
                trail_layout = trail_post["layout"]

                trails.append(models.timeline.TimelinePostTrail(trail_blog, trail_content, trail_layout))
            except KeyError as e:
                logger.warning(f"Unexpected key while parsing post trail for post '{id}'")
                continue

        # Reblogged from data
        reblog_from_information = None
        reblog_root_information = None

        if reblogged_from_id := target.get("rebloggedFromId"):
            reblog_from_information = models.misc.ReblogAttribution(
                post_id=reblogged_from_id,
                post_url=target["rebloggedFromUrl"],
                blog_name=target["rebloggedFromName"],
                blog_title=target["rebloggedFromTitle"],
            )

            if root_reblogged_from_id := target.get("rebloggedRootId"):
                reblog_root_information = models.misc.ReblogAttribution(
                    post_id=root_reblogged_from_id,
                    post_url=target["rebloggedRootUrl"],
                    blog_name=target["rebloggedRootName"],
                    blog_title=target["rebloggedRootTitle"],
                )


        return models.timeline.TimelinePost(
            blog=blog,
            id=id,
            is_nsfw=target["isNsfw"],
            is_advertisement=is_advertisement,
            post_url=target["postUrl"],
            slug=target["slug"],
            date=datetime.datetime.fromtimestamp(target["timestamp"]),
            tags=target["tags"],
            summary=target["summary"],

            content=content,
            layout=layout,
            trail=trails,

            can_like=can_like,
            can_reblog=can_reblog,
            can_reply=can_reply,
            display_avatar=target["displayAvatar"],

            reply_count=reply_count,
            reblog_count=reblog_count,
            like_count=like_count,
            note_count=note_count,

            reblog_from=reblog_from_information,
            reblog_root=reblog_root_information
        )


ELEMENT_PARSERS = (_TimelineBlogParser, _TimelinePostParser)
CONTAINER_PARSERS = (_TimelineParser, _BlogParser)


def parse_item(element, element_index=0, total_elements=1):
    """Parses an item from Tumblr API's JSON response into a more usable structure"""
    item_number = f"({element_index + 1}/{total_elements})"
    logger.debug(f"parse_item: Parsing item {item_number}")

    for parser_index, parser in enumerate(ELEMENT_PARSERS):
        logger.debug(f"parse_item: Attempting to match item {item_number} with `{parser.__name__}`"
                     f"({parser_index + 1}/{len(ELEMENT_PARSERS)})...")

        if parsed_element := parser.process(element):
            return parsed_element

    return None


# TODO refactor into parse_timeline and parse_blog_timeline
def parse_container(initial_data):
    """Parses a container of items from Tumblr API's JSON response into a more usable structure"""
    initial_data = initial_data["response"]
    logger.debug(f"parse_container: Parsing container...")

    for parser_index, parser in enumerate(CONTAINER_PARSERS):
        logger.debug(f"parse_container: Attempting to match container with `{parser.__name__}` "
                     f"({parser_index+1}/{len(CONTAINER_PARSERS)})...")

        if container := parser.process(initial_data):
            logger.debug(f"parse_container: A {type(container).__name__} container has been parsed!")

            return container

    return None
