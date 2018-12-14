from aiohttp import web


async def setup_ws(app):
    app['sockets'] = {}
    app.loop.create_task(broadcast(app))

    async def clean_ws(app):
        for ws in app['sockets'].values():
            await ws.close()

        app['sockets'].clear()

    app.on_cleanup.append(clean_ws)


async def handle_ws_reqs(req):
    socket = web.WebSocketResponse()

    ready = socket.can_prepare(req)
    if not ready.ok:
        return None

    await socket.prepare(req)

    user_id = req.rel_url.query['id']

    if user_id is None:
        await notify_error(socket, 'user id required')
        socket.close()
        return None

    if not await req.app['redis'].sismember('users', user_id):
        await notify_error(socket, 'user id not found')
        socket.close()
        return None

    req.app['sockets'][user_id] = socket
    await handle_socket_msgs(req.app, socket)
    del req.app['sockets'][user_id]

    return socket


async def notify_error(socket, message):
    await socket.send_json({
        'channel': 'pub-error',
        'payload': {
            'error': message
        }})


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
