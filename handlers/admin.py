from pyrogram import filters
from pyrogram.types import Message
from config import ADMIN_IDS
from database import series_col

def register_admin_handlers(app):
    @app.on_message(filters.private & filters.user(ADMIN_IDS) & filters.command("add"))
    async def add_series(client, message: Message):
        try:
            data = message.text.split("\n")[1:]  # Exclude command
            name = data[0].strip()
            season = data[1].strip()
            quality = data[2].strip()
            file_id = message.reply_to_message.document.file_id

            series_col.insert_one({
                "name": name.lower(),
                "season": season,
                "quality": quality,
                "file_id": file_id
            })

            await message.reply("Added successfully.")
        except Exception as e:
            await message.reply(f"Error: {e}")
