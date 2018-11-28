from aiohttp import web
from pub.utils import get_random_hash


async def create_user(req):
    user_id = get_random_hash()
    await req.app['redis'].sadd('users', user_id)
    return web.json_response({
        'status': 'ok',
        'id': user_id
    })


async def sub_channel(req):
    channel = req.match_info['channel']
    user_id = req.rel_url.query['id']

    await req.app['redis'].sadd(channel, user_id)
    return web.json_response({
        'status': 'ok',
        'message': f'Subscribed to channel {channel}'
    })


async def pub_channel(req):
    channel = req.match_info['channel']

    msg = await req.json()

    if not msg['channel'] or not msg['payload']:
        return web.json_response({
            'status': 'error',
            'message': f'Invalid message format'
        }, status=400)

    await req.app['redis'].publish_json('pub-msgs', msg)
    return web.json_response({
        'status': 'ok',
        'message': f'Message published to {channel}'
    })


async def unsub_channel(req):
    channel = req.match_info['channel']
    user_id = req.rel_url.query['id']

    await req.app['redis'].srem(channel, user_id)
    return web.json_response({
        'status': 'ok',
        'message': f'Unsubscribed from {channel}'
    })
