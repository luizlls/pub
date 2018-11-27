from aiohttp import web
from pub.utils import get_random_hash


async def init_wss(app):
    app['websockets'] = {}
    app.loop.create_task(handle_ws_msgs(app))


async def close_wss(app):
    for ws in app['websockets'].values():
        await ws.close()

    app['websockets'].clear()


async def handle_ws_reqs(req):
    socket = web.WebSocketResponse()

    ready = socket.can_prepare(req)
    if not ready.ok:
        return None

    await socket.prepare(req)

    identifier = get_random_hash()

    await socket.send_json({
        'channel': 'pub-notify',
        'payload': {
            'identifier': identifier
        }})

    req.app['websockets'][identifier] = socket
    await handle_incoming_msgs(req.app, socket)
    del req.app['websockets'][identifier]

    return socket


async def handle_incoming_msgs(app, socket):
    while True:
        try:
            msg = await socket.receive_json()
            await app['redis'].publish_json('pub-msgs', msg)
        except Exception:
            break


async def handle_ws_msgs(app):
    channel = (await app['redis'].subscribe('pub-msgs'))[0]

    while await channel.wait_message():
        msg = await channel.get_json()
        print(msg)

    channel.unsubscribe()
