import urllib.parse


def url_handler(raw_url):
    """Change URLs found in posts to privacy-friendly alternatives"""
    url = urllib.parse.urlparse(raw_url)

    hostname = url.hostname

    if hostname.endswith("64.media.tumblr.com"):
        return f"/tblr/media/64{url.path}"
    elif hostname.endswith("assets.tumblr.com"):
        return f"/tblr/assets{url.path}"
    elif hostname.endswith("49.media.tumblr.com"):
        return f"/tblr/media/49{url.path}"
    elif hostname.endswith("44.media.tumblr.com"):
        return f"/tblr/media/44{url.path}"
    elif hostname.endswith("tumblr.com"):
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
            return f"{url.path}"

    return raw_url


