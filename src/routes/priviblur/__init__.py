"""Priviblur specific endpoints"""

import sanic
from .misc import misc_bp

priviblur = sanic.Blueprint.group(misc_bp, url_prefix="/priviblur")