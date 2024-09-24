import datetime

from .. import helpers, models

logger = helpers.LOGGER.getChild("parse")


# TODO refactor module


class BlogThemeParser:
    def __init__(self, target) -> None:
        self.target = target

    @classmethod
    def process(cls, initial_data):
        if theme := initial_data.get("theme"):
            logger.debug("BlogThemeParser: Parser found! Beginning parsing...")
            return cls(theme).parse()
        else:
            return None

    def parse(self):
        # TODO more theme data
        header_info = models.misc.HeaderInfo(
            self.target["headerImage"],
            self.target["headerImageFocused"],
            self.target["headerImageScaled"],
        )

        return models.misc.BlogTheme(
            avatar_shape = self.target["avatarShape"],
            background_color = self.target["backgroundColor"],
            body_font = self.target["bodyFont"],
            header_info=header_info
        )


class BlogInfoParser:
    def __init__(self, target) -> None:
        self.target = target

    @classmethod
    def process(cls, initial_data, force_parse=False):
        if initial_data.get("objectType") == "blog":
            return cls(initial_data["resources"][0]).parse()
        elif force_parse:
            return cls(initial_data).parse()
        else:
            return None

    def parse(self):
        theme = BlogThemeParser.process(self.target)

        return models.timeline.TimelineBlog(
            name=self.target["name"],
            avatar=self.target["avatar"],
            title=self.target["title"],
            url=self.target["url"],
            is_adult=self.target["isAdult"],
            description_npf=self.target["descriptionNpf"],
            uuid=self.target["uuid"],
            theme=theme,
            is_paywall_on=self.target["isPaywallOn"],
            active=self.target.get("active", True)
        )


class TimelinePostParser:
    def __init__(self, target) -> None:
        self.target = target

    @classmethod
    def process(cls, initial_data):
        if initial_data.get("objectType") == "post":
            logger.debug("TimelinePostParser: Parser found! Beginning parsing...")
            return cls(initial_data).parse()
        else:
            return None

    def parse(self):
        blog = BlogInfoParser.process(self.target["blog"], force_parse=True)

        assert blog is not None

        id = self.target["id"]

        note_count = self.target.get("noteCount")
        like_count = None
        reblog_count = None
        reply_count = None

        if can_like := self.target["canReply"]:
            reply_count = self.target["replyCount"]
        if can_reblog := self.target["canReblog"]:
            reblog_count = self.target["reblogCount"]
        if can_reply := self.target["canLike"]:
            like_count = self.target["likeCount"]

        # We check multiple keys as a precautionary measure.
        if self.target.get("advertiserId") or self.target.get("adId") or self.target.get("adProviderId"):
            is_advertisement = True
        else:
            is_advertisement = False

        content = self.target["content"]
        layout = self.target["layout"]
        trail = self.target["trail"]

        trails = []
        for trail_post in trail:
            trail_post_id = None
            trail_post_creation_date = None
            trail_blog = None
            trail_content = None
            trail_layout = None

            has_error = False

            try:
                if raw_trail_blog := trail_post.get("blog"):
                    trail_blog = BlogInfoParser.process(raw_trail_blog, force_parse=True)
                else:
                    trail_blog = models.timeline.BrokenBlog(
                        name=trail_post["brokenBlog"]["name"],
                        avatar=trail_post["brokenBlog"]["avatar"],
                    )
                    
                trail_content = trail_post["content"]
                trail_layout = trail_post["layout"]

                if trail_post_data := trail_post.get("post"):
                    trail_post_id = trail_post_data["id"]
                    trail_post_creation_date = datetime.datetime.fromtimestamp(trail_post_data["timestamp"])

            except KeyError as e:
                logger.warning(f"*: '{e.args[0]}' while parsing post trail for post '{id}' from blog '{blog.name}'")

                if trail_blog is None:
                    trail_blog = models.timeline.BrokenBlog("PriviblurErrorBlog", [
                        {"width": 40, "height": 40, "url": "https://assets.tumblr.com/pop/src/assets/images/avatar/anonymous_avatar_40-3af33dc0.png"},
                        {"width": 96, "height": 96, "url": "https://assets.tumblr.com/pop/src/assets/images/avatar/anonymous_avatar_96-223fabe0.png"}
                    ])

                if trail_content is None:
                    trail_content = (
                        {"type": "text", "text": "Priviblur Parse error", "subtype": "heading1"},
                        {"type": "text", "text": "Error: Priviblur has failed to parse this post"}
                    )

                    # When the contents failed to parse it doesn't make sense to use successfully parsed layouts
                    # thus we'll set it to an empty list. This has also the added benefit of handling when the layouts also
                    # failed to parse
                    trail_layout = []

                # If its just the trail layout that failed to parse then we should also reset it to an empty list
                if trail_layout is None:
                    trail_layout = []

                has_error = True

            trails.append(models.timeline.TimelinePostTrail(
                id=trail_post_id,
                blog=trail_blog,
                date=trail_post_creation_date,
                content=trail_content,
                layout=trail_layout,
                has_error=has_error
            ))


        # Reblogged from data
        reblog_from_information = None
        reblog_root_information = None

        if reblogged_from_id := self.target.get("rebloggedFromId"):
            reblog_from_information = models.misc.ReblogAttribution(
                post_id=reblogged_from_id,
                post_url=self.target["rebloggedFromUrl"],
                blog_name=self.target["rebloggedFromName"],
                blog_title=self.target["rebloggedFromTitle"],
            )

            if root_reblogged_from_id := self.target.get("rebloggedRootId"):
                reblog_root_information = models.misc.ReblogAttribution(
                    post_id=root_reblogged_from_id,
                    post_url=self.target["rebloggedRootUrl"],
                    blog_name=self.target["rebloggedRootName"],
                    blog_title=self.target["rebloggedRootTitle"],
                )

        # Community label
        community_labels = []
        if raw_labels := self.target.get("communityLabels"):
            if raw_labels["hasCommunityLabel"]:
                for category in raw_labels["categories"]:
                    label = getattr(models.timeline.CommunityLabel, category.upper(), None)
                    if label:
                        community_labels.append(label)

                if not community_labels:
                    community_labels.append(models.timeline.CommunityLabel.MATURE)

        return models.timeline.TimelinePost(
            blog=blog,
            id=id,
            is_nsfw=self.target["isNsfw"],
            is_advertisement=is_advertisement,
            post_url=self.target["postUrl"],
            slug=self.target["slug"],
            date=datetime.datetime.fromtimestamp(self.target["timestamp"]),
            tags=self.target["tags"],
            summary=self.target["summary"],

            content=content,
            layout=layout,
            trail=trails,

            can_like=can_like,
            can_reblog=can_reblog,
            can_reply=can_reply,
            display_avatar=self.target["displayAvatar"],

            reply_count=reply_count,
            reblog_count=reblog_count,
            like_count=like_count,
            note_count=note_count,

            reblog_from=reblog_from_information,
            reblog_root=reblog_root_information,

            community_labels=community_labels
        )


def parse_item(element, element_index=0, total_elements=1, use_parsers=[]):
    """Parses an item from Tumblr API's JSON response into a more usable structure"""
    item_number = f"({element_index + 1}/{total_elements})"
    logger.debug(f"parse_item: Parsing item {item_number}")

    for parser_index, parser in enumerate(use_parsers):
        logger.debug(f"parse_item: Attempting to match item {item_number} with `{parser.__name__}`"
                     f"({parser_index + 1}/{len(use_parsers)})...")

        if parsed_element := parser.process(element):
            return parsed_element

    return None
