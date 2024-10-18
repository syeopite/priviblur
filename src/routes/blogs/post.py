import urllib.parse

import sanic
import sanic_ext

from ... import cache, priviblur_extractor

blog_post_bp = sanic.Blueprint("blog_post", url_prefix="/<post_id:int>")


async def render_blog_post(request, blog, post):
    """Handles the logic for rendering viewing a single blog post"""
    blog_info = priviblur_extractor.models.timelines.BlogTimeline(post.blog, (), None, None)

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

# Single post

@blog_post_bp.get("/")
async def _blog_post_no_slug(request: sanic.Request, blog: str, post_id: str):
    blog = urllib.parse.unquote(blog)
    post = (await cache.get_blog_post(request.app.ctx, blog, post_id)).elements[0]

    if post.slug:
        return sanic.redirect(request.app.url_for("blogs._blog_post", blog=blog, post_id=post_id, slug=post.slug, **request.args))
    else:
        return await render_blog_post(request, blog, post)


@blog_post_bp.get("/<slug:str>")
async def _blog_post(request: sanic.Request, blog: str, post_id: str, slug: str):
    blog = urllib.parse.unquote(blog)
    slug = urllib.parse.unquote(slug)

    post = (await cache.get_blog_post(request.app.ctx, blog, post_id)).elements[0]

    # Redirect to the correct slug when the given slug does not match the one of the post
    if post.slug != slug:
        # Unless of course the slug is empty. In that case we'll remove the slug. 
        if post.slug:
            return sanic.redirect(request.app.url_for("blogs._blog_post", blog=blog, post_id=post_id, slug=post.slug, **request.args))
        else:
            return sanic.redirect(request.app.url_for("blogs._blog_post_no_slug", blog=blog, post_id=post_id, **request.args))
    else:
        return await render_blog_post(request, blog, post)
