import pytest


async def test_create_user(client):
    res = await client.post('/api/user')
    assert res.status == 200
    body = await res.json()
    assert body['status'] == 'ok'
    assert len(body['id']) == 32
    pytest.user_id = body['id']


async def test_sub_channel(client):
    url = f'/api/channel/test/sub?id={pytest.user_id}'
    res = await client.post(url)
    assert res.status == 200
    body = await res.json()
    assert body['status'] == 'ok'
    assert body['message'] == 'Subscribed to channel test'


async def test_unsub_channel(client):
    url = f'/api/channel/test/unsub?id={pytest.user_id}'
    res = await client.post(url)
    assert res.status == 200
    body = await res.json()
    assert body['status'] == 'ok'
    assert body['message'] == 'Unsubscribed from test'


async def test_pub_channel(client):
    url = f'/api/channel/test/pub?id={pytest.user_id}'
    res = await client.post(url, json={
        'channel': 'test',
        'payload': {
            'message': 'Test message'
        }
    })
    assert res.status == 200
    body = await res.json()
    assert body['status'] == 'ok'
    assert body['message'] == 'Message published to test'
