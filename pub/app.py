from aiohttp import web
from pub.wss import handle


async def init_app():
    app = web.Application()
    app['websockets'] = {}
    app.on_shutdown.append(shutdown)

    app.add_routes([web.get('/s', handle)])

    return app


async def shutdown(app):
    for ws in app['websockets'].values():
        await ws.close()

    app['websockets'].clear()
