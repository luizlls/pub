from aiohttp import web
from pub.utils import get_random_hash


async def init_wss(app):
    app['sockets'] = {}
    app.loop.create_task(broadcast(app))


async def close_wss(app):
    for ws in app['sockets'].values():
        await ws.close()

    app['sockets'].clear()


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

    req.app['sockets'][identifier] = socket
    await handle_socket_msgs(req.app, socket)
    del req.app['sockets'][identifier]

    return socket


async def handle_socket_msgs(app, socket):
    while True:
        try:
            msg = await socket.receive_json()
            await app['redis'].publish_json('pub-msgs', msg)
        except Exception:
            break


async def broadcast(app):
    channel = (await app['redis'].subscribe('pub-msgs'))[0]

    while await channel.wait_message():
        msg = await channel.get_json()
        ids = await app['redis'].smembers(msg['channel'])
        for id in (i for i in ids if i in app['sockets'].keys()):
            await app['sockets'][id].send_json(msg)

    channel.unsubscribe()
