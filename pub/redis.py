from aioredis import create_redis_pool


async def init_redis(app):
    app['redis'] = await create_redis_pool('redis://localhost')


async def close_redis(app):
    app['redis'].close()
    await app['redis'].wait_closed()
