from aiohttp import web
from pub.routes import setup_routes
from pub.wss import init_wss, close_wss
from pub.redis import init_redis, close_redis


async def init_app():
    app = web.Application()
    app.on_startup.append(init_redis)
    app.on_startup.append(init_wss)
    app.on_cleanup.append(close_redis)
    app.on_cleanup.append(close_wss)

    setup_routes(app)

    return app
