import html
import urllib.parse

import sanic
import sanic_ext

from .. import priviblur_extractor

blogs = sanic.Blueprint("blogs", url_prefix="/<blog:([a-z\d]{1}[a-z\d-]{0,30}[a-z\d]{0,1})>")


async def render_blog_post(app, blog, post):
        return await sanic_ext.render(
            "blog_post.jinja",
            context={
                "app": app,
                "blog": blog,
                "element": post,
            }
        )

@blogs.get("/")
async def _blog_posts(request: sanic.Request, blog: str):
    blog = urllib.parse.unquote(blog)

    if continuation := request.args.get("continuation"):
        continuation = urllib.parse.unquote(continuation)

    if before_id := request.args.get("before_id"):
        continuation = urllib.parse.unquote(before_id)

    initial_results = await request.app.ctx.TumblrAPI.blog_posts(blog, continuation, before_id)
    blog = priviblur_extractor.parse_container(initial_results)

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

    initial_results = await request.app.ctx.TumblrAPI.blog_posts(blog, continuation, tag=tag)
    blog = priviblur_extractor.parse_container(initial_results)

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

    initial_results = await request.app.ctx.TumblrAPI.blog_post(blog, post_id)
    timeline = priviblur_extractor.parse_container(initial_results)
    post = timeline.elements[0]

    if post.slug:
        return sanic.redirect(request.app.url_for("blogs._blog_post", blog=blog, post_id=post_id, slug=post.slug))
    else:
        # Fetch blog info and some posts from before this post
        initial_blog_results = await request.app.ctx.TumblrAPI.blog_posts(blog, before_id=post.id)
        blog_info = priviblur_extractor.parse_container(initial_blog_results)

        return await render_blog_post(request.app, blog_info, post)


@blogs.get("/<post_id:int>/<slug:str>")
async def _blog_post(request: sanic.Request, blog: str, post_id: str, slug: str):
    blog = urllib.parse.unquote(blog)
    slug = urllib.parse.unquote(slug)

    initial_results = await request.app.ctx.TumblrAPI.blog_post(blog, post_id)
    timeline = priviblur_extractor.parse_container(initial_results)
    post = timeline.elements[0]

    # Redirect to the correct slug when the given slug does not match the one of the post
    if post.slug != slug:
        # Unless of course the slug is empty. In that case we'll remove the slug. 
        if post.slug:
            return sanic.redirect(request.app.url_for("blogs._blog_post", blog=blog, post_id=post_id, slug=post.slug))
        else:
            return sanic.redirect(request.app.url_for("blogs._blog_post_no_slug", blog=blog, post_id=post_id))
    else:
        # Fetch blog info and some posts from before this post
        initial_blog_results = await request.app.ctx.TumblrAPI.blog_posts(blog, before_id=post.id)
        blog_info = priviblur_extractor.parse_container(initial_blog_results)

        return await render_blog_post(request.app, blog_info, post)


# Redirects for /post/...

@blogs.get("/post/<post_id:int>")
async def redirect_slash_post_no_slug(request: sanic.Request, blog: str, post_id: str):
    return sanic.redirect(request.app.url_for("blogs._blog_post_no_slug", blog=blog, post_id=post_id))


@blogs.get("/post/<post_id:int>/<slug:str>")
async def redirect_slash_post(request: sanic.Request, blog: str, post_id: str, slug: str):
    return sanic.redirect(request.app.url_for("blogs._blog_post", blog=blog, post_id=post_id, slug=slug))