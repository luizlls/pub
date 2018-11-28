from pub.wss import handle_ws_reqs
from pub.api import create_user, sub_channel, pub_channel, unsub_channel


def setup_routes(app):
    app.router.add_get('/', handle_ws_reqs)
    app.router.add_post('/api/user', create_user)
    app.router.add_post('/api/channel/{channel}/sub', sub_channel)
    app.router.add_post('/api/channel/{channel}/pub', pub_channel)
    app.router.add_post('/api/channel/{channel}/unsub', unsub_channel)
