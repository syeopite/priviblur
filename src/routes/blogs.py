import html
import urllib.parse

import sanic
import sanic_ext

import npf_renderer

from .. import privblur_extractor

blogs = sanic.Blueprint("blogs")


async def render_blog_post(app, post, url_handler):
        return await sanic_ext.render(
            "blog_post.jinja",
            context={
                "app": app,
                "html_escape": html.escape,
                "url_escape": urllib.parse.quote,
                "element": post,
                "url_handler": url_handler,
                "format_npf": npf_renderer.format_npf
            }
        )

@blogs.get("/<blog:str>/<post_id:int>")
async def _blog_post_no_slug(request: sanic.Request, blog: str, post_id: str):
    blog = urllib.parse.unquote(blog)

    initial_results = await request.app.ctx.TumblrAPI.blog_post(blog, post_id)
    timeline = privblur_extractor.parse_container(initial_results)
    post = timeline.elements[0]

    if post.slug:
        return sanic.redirect(request.app.url_for("blogs._blog_post", blog=blog, post_id=post_id, slug=post.slug))
    else:
        return await render_blog_post(request.app, post, request.app.ctx.URL_HANDLER)


@blogs.get("/<blog:str>/<post_id:int>/<slug:str>")
async def _blog_post(request: sanic.Request, blog: str, post_id: str, slug: str):
    blog = urllib.parse.unquote(blog)
    slug = urllib.parse.unquote(slug)

    initial_results = await request.app.ctx.TumblrAPI.blog_post(blog, post_id)
    timeline = privblur_extractor.parse_container(initial_results)
    post = timeline.elements[0]

    # Redirect to the correct slug when the given slug does not match the one of the post
    if post.slug != slug:
        # Unless of course the slug is empty. In that case we'll remove the slug. 
        if post.slug:
            return sanic.redirect(request.app.url_for("blogs._blog_post", blog=blog, post_id=post_id, slug=post.slug))
        else:
            return sanic.redirect(request.app.url_for("blogs._blog_post_no_slug", blog=blog, post_id=post_id))
    else:
        return await render_blog_post(request.app, post, request.app.ctx.URL_HANDLER)
