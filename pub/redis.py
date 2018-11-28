from aioredis import create_redis_pool


async def setup_redis(app):
    pool = await create_redis_pool('redis://localhost', encoding='utf-8')
    app['redis'] = pool

    async def close_redis(app):
        app['redis'].close()
        await app['redis'].wait_closed()

    app.on_cleanup.append(close_redis)
    return pool
