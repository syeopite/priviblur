from sanic import Sanic
import sanic.response

import privblur_extractor
import orjson
import logging

from src.version import VERSION


app = Sanic("Privblur", loads=orjson.loads, dumps=orjson.dumps)


@app.listener("before_server_start")
async def initialize(app):
    # We use the default client for now. But in the future, we'll pass in our own custom
    # aiohttp client when the need arises for it.
    app.ctx.TumblrAPI = await privblur_extractor.TumblrAPI.create(json_loads=orjson.loads)


@app.get("/")
async def root(request):
    return sanic.response.text(VERSION)

if __name__ == "__main__":
    app.run(debug=True)

