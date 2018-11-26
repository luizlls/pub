from aiohttp import web
from pub.utils import get_random_hash
from aioredis import create_redis


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

    while True:
        try:
            msg = await socket.receive_json()
            pub = await create_redis('redis://localhost')
            await pub.publish_json('pub-msgs', msg)
            pub.close()
        except Exception:
            break

    del req.app['websockets'][identifier]

    return socket


async def handle_ws_msgs(app):
    # TODO make redis URL configurable
    sub = await create_redis('redis://localhost')
    channel = (await sub.subscribe('pub-msgs'))[0]
    await read(channel)
    channel.unsubscribe()
    sub.close()


async def read(channel):
    while await channel.wait_message():
        msg = await channel.get_json()
        print(msg)
