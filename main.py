from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/")
async def home(request):
    return web.Response(text="Bot is Running")


def run():
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, port=8080)


if __name__ == "__main__":
    run()
