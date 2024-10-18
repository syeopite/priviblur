import urllib.parse

import sanic
import sanic_ext

from ... import priviblur_extractor
from ...cache import get_blog_posts, get_blog_search_results

blogs = sanic.Blueprint("blogs", url_prefix="/")


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

    blog = priviblur_extractor.models.timelines.BlogTimeline(
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


# Redirects for /post/...

@blogs.get("/post/<post_id:int>")
async def redirect_slash_post_no_slug(request: sanic.Request, blog: str, post_id: str):
    return sanic.redirect(request.app.url_for("blog_post._blog_post", blog=blog, post_id=post_id))


@blogs.get("/post/<post_id:int>/<slug:str>")
async def redirect_slash_post(request: sanic.Request, blog: str, post_id: str, slug: str):
    return sanic.redirect(request.app.url_for("blog_post._blog_post_with_slug", blog=blog, post_id=post_id, slug=slug))
