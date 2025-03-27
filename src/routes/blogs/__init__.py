from sanic import Blueprint

from . import blogs, post

blogs_group = Blueprint.group(
    blogs.blogs, post.blog_post_bp, url_prefix="/<blog:([a-z\d]{1}[a-z\d-]{0,30}[a-z\d]{0,1})>"
)
