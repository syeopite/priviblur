import enum
from typing import NamedTuple


class BlogInfoFieldRequestOptions(NamedTuple):
    """The following controls what information gets sent back as a response when requesting info about a blog.
    If an option is unset via setting it to None, then the information that option represents isn't included.

    The default options are the ones that Tumblr.com uses for requests on /api/v2/explore/*

    Options:
    name:
        Blog name
    avatar:
        Avatar Pictures
    title:
        Blog Title
    url:
        Blog URL
    blog_view_url:
        Blog View URL | "Preview" of the blog when clicking via dashboard
    is_adult:
        Is an NSFW blog
    is_member:
        ?
    description_npf:
        To use Tumblr's new Neue Post Format for not
    uuid:
        Blog ID
    can_be_followed:
        Whether the blog can be followed on Tumblr or not
    followed:
        Whether the requester is following the blog
    advertiser_name:
        ?
    theme:
        The custom theme of the blog. This applies only to the default theme. Actual custom CSS themes are not
        supported
    primary:
        ?
    is_paywall_on:
        Is the blog locked behind paywall?
    paywall_access:
        ? Though I'm guessing this refers to whether or not the blog can be accessed by the requester
    subscription_plan:
        ?
    tumblrmart_accessories:
        Tumblrmart accessories that should be displayed
    share_likes:
        Is the blog sharing their likes?
    share_following:
        Is the blog sharing who they follow?
    can_subscribe:
        ?
    ask:
        Is the ask box enabled?
    can_submit:
        Is the submission box open?
    is_blocked_from_primary:
        ?
    tweet:
        ?
    is_password_protected:
        Is the blog locked behind a password?

    """
    name: bool = True
    avatar: bool = True
    title: bool = True
    url: bool = True
    blog_view_url: bool = True
    is_adult: bool = True
    is_member: bool = True
    description_npf: bool = True
    uuid: bool = True
    can_be_followed: bool = True
    followed: bool = True
    advertiser_name: bool = True
    theme: bool = True
    primary: bool = True
    is_paywall_on: bool = True
    paywall_access: bool = True
    subscription_plan: bool = True
    tumblrmart_accessories: bool = True
    share_likes: bool = True
    share_following: bool = True
    can_subscribe: bool = True
    subscribed: bool = True
    ask: bool = True
    can_submit: bool = True
    is_blocked_from_primary: bool = True
    is_blogless_advertiser: bool = True
    tweet: bool = True
    is_password_protected: bool = True

    # Some parameters have an extra ? for some reason.
    __ENCODING_MAPPER = {
        "is_member": "?is_member",
        "followed": "?followed",
        "advertiser_name": "?advertiser_name",
        "primary": "?primary",
        "is_paywall_on": "?is_paywall_on",
        "paywall_access": "?paywall_access",
        "subscription_plan": "?subscription_plan",
        "can_submit": "?can_submit",
        "is_blocked_from_primary": "?is_blocked_from_primary",
        "is_blogless_advertiser": "?is_blogless_advertiser",
        "tweet": "?tweet",
    }

    def _get_enabled_options(self, change_to_true_name=False):
        """Returns a list of enabled options"""

        fields = []
        field_value_pairs = self._asdict()
        for k, v in field_value_pairs.items():
            # A bool is used to denote if a certain value should be set. Thus, we skip the false ones.
            if v is False:
                continue

            if change_to_true_name and (key_to_add := self.__ENCODING_MAPPER.get(k)):
                fields.append(key_to_add)
            else:
                fields.append(k)

        return fields

    def to_url(self):
        """Returns a URL parameter directory"""
        fields = self._get_enabled_options(change_to_true_name=True)
        return {"fields[blogs]": ','.join(fields)}

    def __str__(self, change_to_true_name=False):
        """Returns a list of enabled options for the string representation"""
        return ','.join(self._get_enabled_options(change_to_true_name))


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


DEFAULT_BLOG_INFO_FIELDS = BlogInfoFieldRequestOptions()

# Default timeline search's fields[blog] is missing te following.
# Also: it seems like share_likes and share_following are switched order-wise but we aren't equipped to deal with that.
# Perhaps something to do for the future: TODO.
TIMELINE_SEARCH_BLOG_INFO_FIELDS = BlogInfoFieldRequestOptions(
    can_subscribe=False, subscribed=False, can_submit=False, is_blocked_from_primary=False,
    is_blogless_advertiser=False, tweet=False, is_password_protected=False
)