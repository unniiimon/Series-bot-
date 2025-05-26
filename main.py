import asyncio
from aiohttp import web
from handlers.bot import bot  # Import your Pyrogram bot instance

routes = web.RouteTableDef()

@routes.get("/")
async def home(request):
    return web.Response(text="Bot is Running")

async def start_services():
    await bot.start()
    print("Bot started")
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("Web server started on http://0.0.0.0:8080")

loop = asyncio.get_event_loop()
loop.run_until_complete(start_services())
loop.run_forever()
