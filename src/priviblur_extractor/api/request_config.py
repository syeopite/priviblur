import enum
from typing import NamedTuple


class ExplorePostTypeFilters(enum.Enum):
    TEXT = 0,
    PHOTOS = 1,
    GIFS = 2,
    QUOTES = 3,
    CHATS = 4,
    AUDIO = 5,
    VIDEO = 6,
    ASKS = 7


class PostTypeFilters(enum.Enum):
    TEXT = 0,
    PHOTO = 1,
    GIF = 2,
    QUOTE = 3,
    LINK = 4,
    CHAT = 5,
    AUDIO = 6,
    VIDEO = 7,
    ANSWER = 8,
    POLL = 9


class TimelineType(enum.Enum):
    TAG = 0
    BLOG = 1
    POST = 2


class ReblogNoteTypes(enum.Enum):
    # Comments and tags
    REBLOGS_WITH_COMMENTS = 0

    # Comments only
    REBLOGS_WITH_CONTENT_COMMENTS = 0

    # Other reblogs
    REBLOGS_ONLY = 0


# Attributes for the fields[blog] request query

EXPLORE_BLOG_INFO_FIELDS = "name,avatar,title,url,blog_view_url,is_adult,?is_member,description_npf,uuid,can_be_followed,?followed,?advertiser_name,theme,?primary,?is_paywall_on,?paywall_access,?subscription_plan,tumblrmart_accessories,can_show_badges,share_likes,share_following,can_subscribe,subscribed,ask,?can_submit,?is_blocked_from_primary,?is_blogless_advertiser,is_password_protected"
TUMBLR_SEARCH_BLOG_INFO_FIELDS = "name,avatar,title,url,blog_view_url,is_adult,?is_member,description_npf,uuid,can_be_followed,?followed,?advertiser_name,theme,?primary,?is_paywall_on,?paywall_access,?subscription_plan,tumblrmart_accessories,can_show_badges,share_following,share_likes,ask"
POST_BLOG_INFO_FIELDS = "name,avatar,title,url,blog_view_url,is_adult,?is_member,description_npf,uuid,can_be_followed,?followed,?advertiser_name,theme,?primary,?is_paywall_on,?paywall_access,?subscription_plan,tumblrmart_accessories,can_show_badges,share_likes,share_following,can_subscribe,subscribed,ask,?can_submit,?is_blocked_from_primary,?analytics_url"
BLOG_POSTS_BLOG_INFO_FIELDS = "	name,avatar,title,url,blog_view_url,is_adult,?is_member,description_npf,uuid,can_be_followed,?followed,?advertiser_name,theme,?primary,?is_paywall_on,?paywall_access,?subscription_plan,tumblrmart_accessories,can_show_badges,share_likes,share_following,can_subscribe,subscribed,ask,?can_submit,?is_blocked_from_primary,?is_blogless_advertiser,is_password_protected,?admin,can_message,ask_page_title,?analytics_url,?top_tags,?allow_search_indexing,is_hidden_from_blog_network,?should_show_tip,?should_show_gift,?should_show_tumblrmart_gift,?can_add_tip_message"
TUMBLR_TAG_BLOG_INFO_FIELDS = EXPLORE_BLOG_INFO_FIELDS
BLOG_SEARCH_BLOG_INFO_FIELDS = EXPLORE_BLOG_INFO_FIELDS