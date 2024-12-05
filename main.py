from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext
import random

# Укажите пути к изображениям
YES_IMAGE = "yes.png"
NO_IMAGE = "no.png"

async def coin_flip(update: Update, context: CallbackContext):
    """Функция для обработки команды /coinflip"""
    result = random.choice(["yes", "no"])
    image_path = YES_IMAGE if result == "yes" else NO_IMAGE
    await update.message.reply_photo(photo=open(image_path, 'rb'))

async def start(update: Update, context: CallbackContext):
    """Обработка команды /start"""
    await update.message.reply_text("Привет! Напиши /coinflip, чтобы подбросить монетку.")

def main():
    # Замените 'YOUR_TOKEN' на токен вашего бота
    application = ApplicationBuilder().token("7919456091:AAHMc4yNQDvyh_nuTH8MdIiGM-8werbXuNE").build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("coinflip", coin_flip))

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
