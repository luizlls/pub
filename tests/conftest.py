from pub.app import init_app
import pytest


def pytest_namespace():
    return {'user_id': ''}


@pytest.fixture
async def client(aiohttp_client):
    app = await init_app()
    return await aiohttp_client(app)
