from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests, os

# Токен бота берём из переменных окружения
BOT_TOKEN = os.getenv("8414030524:AAEAuRaEi6V-xh2xSy5Y1u8X_e7dNebhW1I")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("📍 Отправить локацию", request_location=True)
    markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True)
    await update.message.reply_text(
        "Привет! Отправь мне локацию, и я покажу ближайшие аптеки 💊", 
        reply_markup=markup
    )

# Обработка локации пользователя
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

    # Используем OpenStreetMap (бесплатно)
    url = f"https://nominatim.openstreetmap.org/search.php?q=pharmacy&format=json&lat={latitude}&lon={longitude}&radius=3000"
    response = requests.get(url, headers={'User-Agent': 'TelegramBot'})
    data = response.json()

    if not data:
        await update.message.reply_text("Рядом аптек не найдено 😔")
        return

    result = "Ближайшие аптеки:\n\n"
    for place in data[:5]:  # Показываем максимум 5 ближайших
        name = place.get("display_name", "Аптека")
        lat = place["lat"]
        lon = place["lon"]
        result += f"🏥 {name}\n📍 [Открыть на карте](https://maps.google.com/?q={lat},{lon})\n\n"

    await update.message.reply_text(result, parse_mode="Markdown")

# Создание приложения бота
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.LOCATION, handle_location))

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    app.run_polling()
