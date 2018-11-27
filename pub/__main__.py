import asyncio
import uvloop
from aiohttp import web
from pub.app import init_app


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def main():
    app = init_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
