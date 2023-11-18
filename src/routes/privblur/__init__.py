"""Privblur specific endpoints"""

import sanic
from .misc import misc_bp

privblur = sanic.Blueprint.group(misc_bp, url_prefix="/privblur")