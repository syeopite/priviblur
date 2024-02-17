import html
import urllib.parse

import sanic
import sanic_ext

from .. import priviblur_extractor
from ..cache import get_blog_posts, get_blog_post

blogs = sanic.Blueprint("blogs", url_prefix="/<blog:([a-z\d]{1}[a-z\d-]{0,30}[a-z\d]{0,1})>")


async def render_blog_post(app, blog, post, request_poll_data = False):
        return await sanic_ext.render(
            "blog_post.jinja",
            context={
                "app": app,
                "blog": blog,
                "element": post,
                "request_poll_data" : request_poll_data
            }
        )

@blogs.get("/")
async def _blog_posts(request: sanic.Request, blog: str):
    blog = urllib.parse.unquote(blog)

    if continuation := request.args.get("continuation"):
        continuation = urllib.parse.unquote(continuation)

    if before_id := request.args.get("before_id"):
        continuation = urllib.parse.unquote(before_id)

    blog = await get_blog_posts(request.app.ctx, blog, continuation=continuation, before_id=before_id)

    return await sanic_ext.render(
        "blog.jinja",
        context={
            "app": request.app,
            "blog": blog,
        }
    )


# Tags

@blogs.get("/tagged/<tag:str>")
async def _blog_tags(request: sanic.Request, blog: str, tag: str):
    blog = urllib.parse.unquote(blog)
    tag = urllib.parse.unquote(tag)

    if continuation := request.args.get("continuation"):
        continuation = urllib.parse.unquote(continuation)

    blog = await get_blog_posts(request.app.ctx, blog, continuation=continuation, tag=tag)

    return await sanic_ext.render(
        "blog.jinja",
        context={
            "app": request.app,
            "blog": blog,
            "tag": tag,
        }
    )


# Single post

@blogs.get("/<post_id:int>")
async def _blog_post_no_slug(request: sanic.Request, blog: str, post_id: str):
    blog = urllib.parse.unquote(blog)
    post = (await get_blog_post(request.app.ctx, blog, post_id)).elements[0]

    if post.slug:
        return sanic.redirect(request.app.url_for("blogs._blog_post", blog=blog, post_id=post_id, slug=post.slug, **request.args))
    else:
        # Fetch blog info and some posts from before this post
        blog_info = await get_blog_posts(request.app.ctx, blog, before_id=post.id)

        if request.args.get("fetch_polls") in {1, "true"}:
            fetch_poll_results = True
        else:
            fetch_poll_results = False

        return await render_blog_post(request.app, blog_info, post, fetch_poll_results)


@blogs.get("/<post_id:int>/<slug:str>")
async def _blog_post(request: sanic.Request, blog: str, post_id: str, slug: str):
    blog = urllib.parse.unquote(blog)
    slug = urllib.parse.unquote(slug)

    post = (await get_blog_post(request.app.ctx, blog, post_id)).elements[0]

    # Redirect to the correct slug when the given slug does not match the one of the post
    if post.slug != slug:
        # Unless of course the slug is empty. In that case we'll remove the slug. 
        if post.slug:
            return sanic.redirect(request.app.url_for("blogs._blog_post", blog=blog, post_id=post_id, slug=post.slug, **request.args))
        else:
            return sanic.redirect(request.app.url_for("blogs._blog_post_no_slug", blog=blog, post_id=post_id, **request.args))
    else:
        # Fetch blog info and some posts from before this post
        blog_info = await get_blog_posts(request.app.ctx, blog, before_id=post.id)

        if request.args.get("fetch_polls") in ("1", "true"):
            fetch_poll_results = True
        else:
            fetch_poll_results = False

        return await render_blog_post(request.app, blog_info, post, fetch_poll_results)


# Redirects for /post/...

@blogs.get("/post/<post_id:int>")
async def redirect_slash_post_no_slug(request: sanic.Request, blog: str, post_id: str):
    return sanic.redirect(request.app.url_for("blogs._blog_post_no_slug", blog=blog, post_id=post_id))


@blogs.get("/post/<post_id:int>/<slug:str>")
async def redirect_slash_post(request: sanic.Request, blog: str, post_id: str, slug: str):
    return sanic.redirect(request.app.url_for("blogs._blog_post", blog=blog, post_id=post_id, slug=slug))