import datetime
import copy
import urllib.parse
from typing import Sequence

import sanic

from ..cache import get_poll_results


def url_handler(raw_url):
    """Change URLs found in posts to privacy-friendly alternatives"""
    url = urllib.parse.urlparse(raw_url)

    hostname = url.hostname

    # Redirects links can have malformed URLs such as https://href.li/?http://
    # As those are not proper links by themselves, we'll just use the entire
    # redirect link.
    try:
        if hostname.endswith("href.li"):
            return url_handler(url.query)
        elif hostname.endswith("t.umblr.com"):
            parsed_query = urllib.parse.parse_qs(url.query)
            if redirect_url := parsed_query.get("z"):
                return url_handler(redirect_url[0])
    except AttributeError:
        pass

    if hostname.endswith("tumblr.com"):
        if hostname.endswith(".media.tumblr.com"):
            sub_domains = hostname.split(".")
            if sub_domains[1] == "media":
                return f"/tblr/media/{sub_domains[0]}{url.path}"
            elif sub_domains[0] == "www" and sub_domains[2] == "media":
                return f"/tblr/media/{sub_domains[1]}{url.path}"

        # Continue down the chain when the above doesn't match
        if hostname.endswith("assets.tumblr.com"):
            return f"/tblr/assets{url.path}"
        elif hostname.endswith("static.tumblr.com"):
            return f"/tblr/static{url.path}"
        elif hostname.startswith("a."):
            return f"/tblr/a{url.path}"
        else:
            # Check for subdomain blog
            sub_domains = hostname.split(".")

            if sub_domains[0] == "www":
                potential_blog_name = sub_domains[1]
            else:
                potential_blog_name = sub_domains[0]

            # Check if blog
            if potential_blog_name != "tumblr":
                if url.path.startswith("/post"):
                    return f"/{potential_blog_name}{url.path[5:]}"
                else:
                    return f"/{potential_blog_name}{url.path}"
            else:
                return f"{url.path}"

    return raw_url


def update_query_params(base_query_args, key, value):
    """Returns a URL query string with a parameter replaced/added"""
    base_query_args = copy.copy(base_query_args)

    if isinstance(value, Sequence):
        base_query_args[key] = value
    else:
        base_query_args[key] = [value]

    return urllib.parse.urlencode(base_query_args, doseq=True)


def remove_query_params(base_query_args, key):
    """Returns a URL query string with a parameter replaced/added"""
    base_query_args = copy.copy(base_query_args)

    if base_query_args.get(key):
        del base_query_args[key]

    return urllib.parse.urlencode(base_query_args, doseq=True)


def deseq_urlencode(query_args):
    return urllib.parse.urlencode(query_args, doseq=True)


def prefix_slash_in_url_if_missing(url):
    if not url.startswith("/"):
        return f"/{url}"
    else:
        return f"/{url.lstrip("/")}"


async def create_poll_callback(ctx, blog, post_id):
    async def poll_callable(poll_id, expiration_timestamp):
        current_timestamp = round(datetime.datetime.utcnow().timestamp())
        expired = current_timestamp > expiration_timestamp

        return await get_poll_results(ctx, blog, post_id, poll_id, expired=expired)

    return poll_callable