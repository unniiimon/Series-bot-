import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URL = os.getenv("MONGO_URL")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split()))
FILES_CHANNEL = os.getenv("FILES_CHANNEL")  # optional channel for file input
