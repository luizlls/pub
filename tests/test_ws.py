import pytest


async def test_pub_ws(client):
    async with client.ws_connect(f'/?id={pytest.user_id}') as ws:
        await ws.send_json({
            'channel': 'test',
            'payload': {
                'message': 'Test message WS client'
            }
        })

        await ws.close()
