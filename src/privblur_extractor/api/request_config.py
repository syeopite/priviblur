import enum
from typing import NamedTuple


class PostType(enum.Enum):
    TEXT = 0,
    PHOTOS = 1,
    GIFS = 2,
    QUOTES = 3,
    CHATS = 4,
    AUDIO = 5,
    VIDEO = 6,
    ASKS = 7


class TimelineType(enum.Enum):
    TAG = 0
    BLOG = 1
    POST = 2


# Attributes for the fields[blog] request query

EXPLORE_BLOG_INFO_FIELDS = "name,avatar,title,url,blog_view_url,is_adult,?is_member,description_npf,uuid,can_be_followed,?followed,?advertiser_name,theme,?primary,?is_paywall_on,?paywall_access,?subscription_plan,tumblrmart_accessories,?live_now,can_show_badges,share_likes,share_following,can_subscribe,subscribed,ask,?can_submit,?is_blocked_from_primary,?is_blogless_advertiser,is_password_protected"
TUMBLR_SEARCH_BLOG_INFO_FIELDS = "name,avatar,title,url,blog_view_url,is_adult,?is_member,description_npf,uuid,can_be_followed,?followed,?advertiser_name,theme,?primary,?is_paywall_on,?paywall_access,?subscription_plan,tumblrmart_accessories,?live_now,can_show_badges,share_following,share_likes,ask"
