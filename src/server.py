import logging

from sanic import Sanic
import sanic.response
import orjson
from privblur_extractor import TumblrAPI, parse_item, parse_container

from helpers import setup_logging
from version import VERSION
import routes

setup_logging.setup_logging(logging.WARN)

app = Sanic("Privblur", loads=orjson.loads, dumps=orjson.dumps)
app.ctx.LOGGER = logging.getLogger("privblur")
app.ctx.VERSION = VERSION


@app.listener("before_server_start")
async def initialize(app):
    # We use the default client for now. But in the future, we'll pass in our own custom
    # aiohttp client when the need arises for it.
    app.ctx.TumblrAPI = await TumblrAPI.create(json_loads=orjson.loads)


@app.listener("main_process_start")
async def main_startup_listener(app):
    """Startup listener to notify of privblur startup"""
    # Are we able to print colored output? If so we do it.
    try:
        import colorful
    except ImportError:
        colorful = None

    if not colorful:
        print(f"Starting up Privblur version {VERSION}")
    else:
        print(f"{colorful.green('Launching up')} {colorful.cyan('Privblur')} "
              f"{colorful.bold(f'{VERSION}')}")


@app.get("/")
async def root(request):
    return sanic.response.text(VERSION)


# Register all routes:
for route in routes.BLUEPRINTS:
    app.blueprint(route)


if __name__ == "__main__":
    app.run(debug=True)

