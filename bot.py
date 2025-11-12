import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8414030524:AAEAuRaEi6V-xh2xSy5Y1u8X_e7dNebhW1I" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне локацию, и я покажу ближайшие аптеки 🏥")

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lat = update.message.location.latitude
    lon = update.message.location.longitude

    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      node["amenity"="pharmacy"](around:3000,{lat},{lon});
      way["amenity"="pharmacy"](around:3000,{lat},{lon});
      relation["amenity"="pharmacy"](around:3000,{lat},{lon});
    );
    out center;
    """
    response = requests.get(overpass_url, params={'data': query})
    data = response.json()

    if not data['elements']:
        await update.message.reply_text("Рядом аптек не найдено 😔")
        return

    reply_text = "Ближайшие аптеки:\n\n"
    for el in data['elements'][:5]:
        if 'lat' in el:
            lat_, lon_ = el['lat'], el['lon']
        else:
            lat_, lon_ = el['center']['lat'], el['center']['lon']
        name = el['tags'].get('name', 'Без названия')
        reply_text += f"🏥 {name}\n📍 https://maps.google.com/?q={lat_},{lon_}\n\n"

    await update.message.reply_text(reply_text)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.LOCATION, location))
app.run_polling()
