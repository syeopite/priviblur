import urllib.parse


def url_handler(raw_url):
    """Change URLs found in posts to privacy-friendly alternatives"""
    url = urllib.parse.urlparse(raw_url)

    if url.hostname.endswith("64.media.tumblr.com"):
        return f"/media/image{url.path}"

    return raw_url


