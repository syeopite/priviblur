from sanic import Blueprint

from .misc import misc

v1 = Blueprint.group(misc, url_prefix="/v1")
