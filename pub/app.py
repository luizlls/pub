from aiohttp import web
from pub.routes import setup_routes
from pub.ws import setup_ws
from pub.redis import setup_redis


async def init_app():
    app = web.Application()
    setup_routes(app)
    app.on_startup.extend([setup_redis, setup_ws])

    return app
