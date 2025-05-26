from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers import admin, user

app = Client("series_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

admin.register_admin_handlers(app)
user.register_user_handlers(app)

app.run()
