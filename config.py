import os

API_ID = int(os.getenv("20285891"))
API_HASH = os.getenv("91cc4499bae62106f16024cfa45fa2b3")
BOT_TOKEN = os.getenv("5592785179:AAFx8NbYObOPuj9Pyp0KK-mijn-784zSc9w")
MONGO_URI = os.getenv("mongodb+srv://fepid88067:Bkp3bgslZPJ74Dcu@cluster0.h7ljpgb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "1426582599").split()))
