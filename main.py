from aiohttp import web
import asyncio
from handlers.bot import run_bot  # Import from folder

routes = web.RouteTableDef()

@routes.get("/")
async def home(request):
    return web.Response(text="Bot is Running")

async def start_services():
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    app = web.Application()
    app.add_routes(routes)
    return app

if __name__ == "__main__":
    web.run_app(start_services(), port=8080)
