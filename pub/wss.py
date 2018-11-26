import aiohttp
from pub.utils import get_random_hash


async def handle(request):
    socket = aiohttp.web.WebSocketResponse()

    ready = socket.can_prepare(request)
    if not ready.ok:
        return None

    await socket.prepare(request)

    identifier = get_random_hash()

    await socket.send_json({
        'channel': 'pub-notify',
        'message': {
            'identifier': identifier
        }})

    request.app['websockets'][identifier] = socket

    while True:
        msg = await socket.receive()

        if msg.type == aiohttp.WSMsgType.text:
            print(msg.data)
        else:
            break

    del request.app['websockets'][identifier]

    return socket
