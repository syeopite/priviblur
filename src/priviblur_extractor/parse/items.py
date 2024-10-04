
"""Parses individual items from Tumblr's JSON API into an object"""


import datetime

from .. import helpers, models

logger = helpers.LOGGER.getChild("parse")


class BlogParser:
    def __init__(self, target) -> None:
        self.target = target

    @classmethod
    def process(cls, initial_data):
        if initial_data.get("objectType") == "blog":
            return cls(initial_data["resources"][0]).parse()
        else:
            return None

    def parse_theme(self):
        """Parses theming information for the blog into a BlogTheme object"""
        target = self.target.get("theme")

        header_info = models.blog.HeaderInfo(
            target["headerImage"],
            target["headerImageFocused"],
            target["headerImageScaled"],
        )

        return models.blog.BlogTheme(
            avatar_shape = target["avatarShape"],
            background_color = target["backgroundColor"],
            body_font = target["bodyFont"],
            header_info=header_info
        )

    def parse(self):
        return models.blog.Blog(
            name=self.target["name"],
            avatar=self.target["avatar"],
            title=self.target["title"],
            url=self.target["url"],
            is_adult=self.target["isAdult"],
            description_npf=self.target["descriptionNpf"],
            uuid=self.target["uuid"],
            theme=self.parse_theme(),
            is_paywall_on=self.target["isPaywallOn"],
            active=self.target.get("active", True)
        )


class PostParser:
    def __init__(self, target) -> None:
        self.target = target

    @classmethod
    def process(cls, initial_data):
        if initial_data.get("objectType") == "post":
            return cls(initial_data).parse()
        else:
            return None

    def parse(self):
        # When we know that the target is a blog object there is no need to
        # pass it to .process to identify it
        blog = BlogParser(self.target["blog"]).parse()

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
            is_broken_trail = False

            if raw_trail_blog := trail_post.get("blog"):
                trail_blog = BlogParser(raw_trail_blog).parse()
            else:
                trail_blog = models.blog.BrokenBlog(
                    name=trail_post["brokenBlog"]["name"],
                    avatar=trail_post["brokenBlog"]["avatar"],
                )

                is_broken_trail = True

            trail_content = trail_post["content"]
            trail_layout = trail_post["layout"]

            if (trail_post_data := trail_post.get("post")) and not is_broken_trail:
                trail_post_id = trail_post_data["id"]
                trail_post_creation_date = datetime.datetime.fromtimestamp(trail_post_data["timestamp"])
            else:
                trail_post_id = None
                trail_post_creation_date = None

            trails.append(models.post.PostTrail(
                id=trail_post_id,
                blog=trail_blog,
                date=trail_post_creation_date,
                content=trail_content,
                layout=trail_layout,
            ))


        # Reblogged from data
        reblog_from_information = None
        reblog_root_information = None

        if reblogged_from_id := self.target.get("rebloggedFromId"):
            reblog_from_information = models.post.ReblogAttribution(
                post_id=reblogged_from_id,
                post_url=self.target["rebloggedFromUrl"],
                blog_name=self.target["rebloggedFromName"],
                blog_title=self.target["rebloggedFromTitle"],
            )

            if root_reblogged_from_id := self.target.get("rebloggedRootId"):
                reblog_root_information = models.post.ReblogAttribution(
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
                    label = getattr(models.post.CommunityLabel, category.upper(), None)
                    if label:
                        community_labels.append(label)

                if not community_labels:
                    community_labels.append(models.post.CommunityLabel.MATURE)

        return models.post.Post(
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


def parse_item(element, element_index=0, total_elements=1, use_parsers=None):
    """Parses an item from Tumblr API's JSON response into a more usable structure"""
    item_number = f"({element_index + 1}/{total_elements})"
    logger.debug(f"parse_item: Parsing item {item_number}")

    if not use_parsers:
        return PostParser.process(element)

    # use_parsers must be a iterable object
    for parser_index, parser in enumerate(use_parsers):
        logger.debug(f"parse_item: Attempting to match item {item_number} with `{parser.__name__}`"
                     f"({parser_index + 1}/{len(use_parsers)})...")

        if parsed_element := parser.process(element):
            return parsed_element

    return None
