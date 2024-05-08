import html
import urllib.parse

import sanic
import sanic_ext

from .. import priviblur_extractor
from ..cache import get_blog_posts, get_blog_post, get_blog_search_results

blogs = sanic.Blueprint("blogs", url_prefix="/<blog:([a-z\d]{1}[a-z\d-]{0,30}[a-z\d]{0,1})>")


async def render_blog_post(request, blog, post):
    """Handles the logic for rendering viewing a single blog post"""
    blog_info = priviblur_extractor.models.blog.Blog(post.blog, (), None, None)

    if request.args.get("fetch_polls") in ("1", "true"):
        fetch_poll_results = True
    else:
        fetch_poll_results = False

    return await sanic_ext.render(
        "blog/blog_post.jinja",
        context={
            "app": request.app,
            "blog": blog_info,
            "element": post,
            "request_poll_data" : fetch_poll_results,
        }
    )


@blogs.get("/")
async def _blog_posts(request: sanic.Request, blog: str):
    blog = urllib.parse.unquote(blog)

    if continuation := request.args.get("continuation"):
        continuation = urllib.parse.unquote(continuation)

    if before_id := request.args.get("before_id"):
        before_id = urllib.parse.unquote(before_id)

    blog = await get_blog_posts(request.app.ctx, blog, continuation=continuation, before_id=before_id)

    return await sanic_ext.render(
        "blog/blog.jinja",
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
        "blog/blog.jinja",
        context={
            "app": request.app,
            "blog": blog,
            "tag": tag,
        }
    )


# Search

@blogs.get("/search/<query:str>")
async def _blog_search(request: sanic.Request, blog: str, query: str):
    blog = urllib.parse.unquote(blog)
    query = urllib.parse.unquote(query)

    try:
        if page := request.args.get("page"):
            page = int(urllib.parse.unquote(page))
    except ValueError:
        page = None

    post_list = (await get_blog_search_results(request.app.ctx, blog, query, page=page))
    blog_info = (await get_blog_posts(request.app.ctx, blog)).blog_info

    blog = priviblur_extractor.models.blog.Blog(
        blog_info=blog_info,
        posts = post_list,
        total_posts=None,
        next=None
    )

    return await sanic_ext.render(
        "blog/blog_search.jinja",
        context={
            "app": request.app,
            "blog": blog,
            "blog_search_query": query,
            "page": page,
        }
    )


@blogs.get("/search")
async def query_param_redirect(request: sanic.Request, blog: str):
    """Endpoint for /search to redirect q= queries to /search/<query>"""
    if query := request.args.get("q"):
        return sanic.redirect(request.app.url_for("blogs._blog_search", blog=blog, query=urllib.parse.quote(query, safe="")))
    else:
        return sanic.redirect(request.app.url_for("blogs._blog_posts", blog=blog))


# Single post

@blogs.get("/<post_id:int>")
async def _blog_post_no_slug(request: sanic.Request, blog: str, post_id: str):
    blog = urllib.parse.unquote(blog)
    post = (await get_blog_post(request.app.ctx, blog, post_id)).elements[0]

    if post.slug:
        return sanic.redirect(request.app.url_for("blogs._blog_post", blog=blog, post_id=post_id, slug=post.slug, **request.args))
    else:
        return await render_blog_post(request, blog, post)


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
        return await render_blog_post(request, blog, post)


# Redirects for /post/...

@blogs.get("/post/<post_id:int>")
async def redirect_slash_post_no_slug(request: sanic.Request, blog: str, post_id: str):
    return sanic.redirect(request.app.url_for("blogs._blog_post_no_slug", blog=blog, post_id=post_id))


@blogs.get("/post/<post_id:int>/<slug:str>")
async def redirect_slash_post(request: sanic.Request, blog: str, post_id: str, slug: str):
    return sanic.redirect(request.app.url_for("blogs._blog_post", blog=blog, post_id=post_id, slug=slug))
