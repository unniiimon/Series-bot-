from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_IDS, FILES_CHANNEL
from database import get_series_collection

bot = Client("series-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    await message.reply("Welcome to the Series Bot! Send series name to search.")

@bot.on_message(filters.private & filters.text & ~filters.command("start"))
async def search_handler(client, message: Message):
    query = message.text.strip()
    series_col = get_series_collection()
    series = await series_col.find_one({"name": query})
    if not series:
        await message.reply("Series not found.")
        return
    seasons = list(series["data"].keys())
    buttons = [[InlineKeyboardButton(text=season, callback_data=f"season|{query}|{season}")] for season in seasons]
    await message.reply("Select Season:", reply_markup=InlineKeyboardMarkup(buttons))

@bot.on_callback_query(filters.regex("^season\|"))
async def season_callback(client, callback_query):
    _, series, season = callback_query.data.split("|")
    series_col = get_series_collection()
    data = await series_col.find_one({"name": series})
    qualities = list(data["data"][season].keys())
    buttons = [[InlineKeyboardButton(text=q, callback_data=f"quality|{series}|{season}|{q}")] for q in qualities]
    await callback_query.message.edit_text("Select Quality:", reply_markup=InlineKeyboardMarkup(buttons))

@bot.on_callback_query(filters.regex("^quality\|"))
async def quality_callback(client, callback_query):
    _, series, season, quality = callback_query.data.split("|")
    series_col = get_series_collection()
    data = await series_col.find_one({"name": series})
    file_ids = data["data"][season][quality]
    for file_id in file_ids:
        await client.send_cached_media(callback_query.from_user.id, file_id)
    await callback_query.message.edit_text("Files sent to your PM")


# Admin file upload via channel
@bot.on_message(filters.channel & filters.document & filters.chat(FILES_CHANNEL))
async def handle_channel_upload(client, message: Message):
    caption = message.caption  # Expected format: Series Name | Season | Quality
    if not caption or "|" not in caption:
        return
    try:
        name, season, quality = map(str.strip, caption.split("|"))
    except:
        return

    series_col = get_series_collection()
    doc_id = message.document.file_id
    existing = await series_col.find_one({"name": name})
    if existing:
        existing["data"].setdefault(season, {}).setdefault(quality, []).append(doc_id)
        await series_col.update_one({"name": name}, {"$set": {"data": existing["data"]}})
    else:
        await series_col.insert_one({"name": name, "data": {season: {quality: [doc_id]}}})

async def run_bot():
    await bot.start()
        
