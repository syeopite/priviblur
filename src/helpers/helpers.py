import urllib.parse


def url_handler(raw_url):
    """Change URLs found in posts to privacy-friendly alternatives"""
    url = urllib.parse.urlparse(raw_url)

    if url.hostname.endswith("64.media.tumblr.com"):
        return f"/tblr/media/64{url.path}"
    elif url.hostname.endswith("assets.tumblr.com"):
        return f"/tblr/assets{url.path}"
    elif url.hostname.endswith("49.media.tumblr.com"):
        return f"/tblr/media/49{url.path}"

    return raw_url


