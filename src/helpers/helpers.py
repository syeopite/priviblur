import copy
import urllib.parse
from typing import Sequence

import sanic

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
        if hostname.endswith("64.media.tumblr.com"):
            return f"/tblr/media/64{url.path}"
        elif hostname.endswith("assets.tumblr.com"):
            return f"/tblr/assets{url.path}"
        elif hostname.endswith("49.media.tumblr.com"):
            return f"/tblr/media/49{url.path}"
        elif hostname.endswith("44.media.tumblr.com"):
            return f"/tblr/media/44{url.path}"
        elif hostname.endswith("static.tumblr.com"):
            return f"/tblr/static{url.path}"
        elif hostname.startswith("va.media"):
            return f"/tblr/media/va{url.path}"
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


def translate(language, id, number=None, substitution=None):
    app = sanic.Sanic.get_app("Priviblur")

    gettext_instance = app.ctx.GETTEXT_INSTANCES[language]

    if number is not None:
        translated = gettext_instance.ngettext(id, f"{id}_plural", number)
    else:
        translated = gettext_instance.gettext(id)

    if substitution:
        translated = translated.format(substitution)

    return translated 
    