import datetime
from typing import Optional, Dict, Any

import sanic
import sanic_ext


# Wrapper around sanic_ext.render
async def render_template(template: str = "", context: Optional[Dict[str, Any]] = None, **kwargs):
    jinja_context = context or {}
    # Append additional context

    request = sanic.Request.get_current()

    jinja_context.update(getattr(request.ctx, "breq_jinja_context", {}))

    if request.route and hasattr(request.route.ctx, "rss") or hasattr(request.ctx, "rss"):
        template = getattr(request.route.ctx, "template", None) or template
        template = f"rss/{template}.xml"
        kwargs["content_type"] = "application/rss+xml"

        if not (page_url := getattr(request.ctx, "page_url", None)):
            base_path = request.app.url_for(request.endpoint[:-4], **request.match_info)

            page_url = f"{request.app.ctx.PRIVIBLUR_CONFIG.deployment.domain or ''}{base_path}"
            if request.query_string:
                page_url += f"?{request.query_string}"

        jinja_context["page_url"] = page_url

        if (elements := jinja_context.get("blog")) and elements.posts:
            jinja_context["updated"] = elements.posts[-1].date
        elif (elements := jinja_context.get("timeline")) and elements.elements:
            jinja_context["updated"] = elements.elements[-1].date
        elif (elements := jinja_context.get("notes")) and elements.notes:
            jinja_context["updated"] = elements.notes[-1].date
        else:
            jinja_context["updated"] = datetime.datetime.now(tz=datetime.timezone.utc)

    template = f"{template}.jinja"

    return await sanic_ext.render(template, context=jinja_context, app=request.app, **kwargs)
