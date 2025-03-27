from sanic import Blueprint
from .v1 import v1

api = Blueprint.group(v1, url_prefix="/api")
