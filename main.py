from telegram import Update, InlineQueryResultPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, InlineQueryHandler, CallbackContext
import random

# Укажите пути к изображениям
YES_IMAGE = "yes.png"
NO_IMAGE = "no.png"

async def inline_query(update: Update, context: CallbackContext):
    """Обработка inline-запросов"""
    query = update.inline_query.query

    # Результат подбрасывания монетки
    result = random.choice(["yes", "no"])
    image_url = YES_IMAGE if result == "yes" else NO_IMAGE
    title = "Да" if result == "yes" else "Нет"

    # Создаем результат для отправки
    results = [
        InlineQueryResultPhoto(
            id="1",
            title=title,
            photo_url=image_url,
            caption=f"Монетка говорит: {title}!"
        )
    ]

    await update.inline_query.answer(results, cache_time=0)

async def start(update: Update, context: CallbackContext):
    """Обработка команды /start"""
    await update.message.reply_text("Привет! Используй @<имя_бота>, чтобы подбросить монетку.")

def main():
    # Замените 'YOUR_TOKEN' на токен вашего бота
    application = ApplicationBuilder().token("7919456091:AAHMc4yNQDvyh_nuTH8MdIiGM-8werbXuNE").build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(InlineQueryHandler(inline_query))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
