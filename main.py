from telegram import Update, InlineQueryResultPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, InlineQueryHandler, CallbackContext
import random
import logging

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Укажите правильные URL для изображений из вашего репозитория GitHub
YES_IMAGE = "https://i0.wp.com/bariatric.ru/su_sv/wp-content/uploads/2017/10/yes.png?fit=700%2C300&amp;ssl=1&amp;w=640"
NO_IMAGE = "https://nklk.ru/dll_image/4738.png"

async def inline_query(update: Update, context: CallbackContext):
    """Обработка inline-запросов"""
    try:
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
                thumbnail_url=image_url,  # Добавляем миниатюру
                caption=f"Монетка говорит: {title}!"
            )
        ]
        
        await update.inline_query.answer(results, cache_time=0)
    except Exception as e:
        logger.error(f"Ошибка при обработке inline запроса: {e}")
        await update.inline_query.answer([])  # Отправляем пустой ответ в случае ошибки

async def start(update: Update, context: CallbackContext):
    """Обработка команды /start"""
    await update.message.reply_text("Привет! Используй @<имя_бота>, чтобы подбросить монетку.")

def main():
    """Основная функция для запуска бота"""
    # Замените 'YOUR_TOKEN' на токен вашего бота
    application = ApplicationBuilder().token("7919456091:AAHMc4yNQDvyh_nuTH8MdIiGM-8werbXuNE").build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(InlineQueryHandler(inline_query))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
