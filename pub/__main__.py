from aiohttp import web
from pub.app import init_app


def main():
    app = init_app()
    web.run_app(app, port='3000')


if __name__ == '__main__':
    main()
