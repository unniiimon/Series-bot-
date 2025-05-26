from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import series_col

def register_user_handlers(app):
    @app.on_message(filters.private | filters.group)
    async def get_series(client, message: Message):
        if not message.text:
            return
        name = message.text.strip().lower()
        results = series_col.find({"name": name})
        seasons = sorted(set([r['season'] for r in results]))

        if not seasons:
            await message.reply("Series not found.")
            return

        buttons = [[InlineKeyboardButton(season, callback_data=f"season|{name}|{season}")]
                   for season in seasons]
        await message.reply("Choose a season:", reply_markup=InlineKeyboardMarkup(buttons))

    @app.on_callback_query(filters.regex("^season\|"))
    async def season_handler(client, callback):
        _, name, season = callback.data.split("|")
        results = series_col.find({"name": name, "season": season})
        qualities = sorted(set([r['quality'] for r in results]))

        buttons = [[InlineKeyboardButton(q, callback_data=f"quality|{name}|{season}|{q}")]
                   for q in qualities]
        await callback.message.edit("Choose a quality:", reply_markup=InlineKeyboardMarkup(buttons))

    @app.on_callback_query(filters.regex("^quality\|"))
    async def quality_handler(client, callback):
        _, name, season, quality = callback.data.split("|")
        files = series_col.find({"name": name, "season": season, "quality": quality})

        for f in files:
            await client.send_document(chat_id=callback.from_user.id, document=f['file_id'])

        await callback.message.edit("Sent files to your DM.")
