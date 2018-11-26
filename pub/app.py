from aiohttp import web
from pub.wss import init_wss, close_wss, handle_ws_reqs


async def init_app():
    app = web.Application()
    app.on_startup.append(init_wss)
    app.on_cleanup.append(close_wss)

    app.add_routes([
        web.get('/wss', handle_ws_reqs)])

    return app
