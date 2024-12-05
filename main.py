from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InputMediaPhoto,
)
from telegram.ext import ApplicationBuilder, CommandHandler, InlineQueryHandler, CallbackContext
import random
import logging
import uuid

# Настройка логирования
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# URL для заблюренных изображений
YES_IMAGE = "https://nklk.ru/dll_image/4738.png" 
NO_IMAGE = "https://nklk.ru/dll_image/4739.png"   

async def inline_query(update: Update, context: CallbackContext):
    """Обработка inline-запросов"""
    try:
        # Создаем инлайн-результат с текстом "Подбросить монетку"
        results = [
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),  # Уникальный идентификатор
                title="Подбросить монетку",
                input_message_content=InputTextMessageContent(
                    "Подбрасываем монетку... 🪙", parse_mode="HTML"
                ),  # Скрытый текст при отправке
            )
        ]

        await update.inline_query.answer(results, cache_time=0)
    except Exception as e:
        logger.error(f"Ошибка при обработке inline-запроса: {e}")
        await update.inline_query.answer([])  # Отправляем пустой ответ в случае ошибки

async def send_coin_result(update: Update, context: CallbackContext):
    """Отправляет результат подбрасывания монетки"""
    try:
        # Результат подбрасывания монетки
        result = random.choice(["yes", "no"])
        image_url = YES_IMAGE if result == "yes" else NO_IMAGE
        title = "Да" if result == "yes" else "Нет"

        # Отправляем картинку с текстом
        await update.message.reply_photo(
            photo=image_url,
            caption=f"<b>Монетка говорит:</b> {title}!",
            parse_mode="HTML",
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке результата: {e}")
        await update.message.reply_text("Произошла ошибка. Попробуйте снова!")

async def start(update: Update, context: CallbackContext):
    """Обработка команды /start"""
    await update.message.reply_text(
        "Привет! Используй @<имя_бота>, чтобы подбросить монетку."
    )

def main():
    """Основная функция для запуска бота"""
    # Замените 'YOUR_TOKEN' на токен вашего бота
    application = ApplicationBuilder().token("7919456091:AAHMc4yNQDvyh_nuTH8MdIiGM-8werbXuNE").build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(InlineQueryHandler(inline_query))
    application.add_handler(CommandHandler("flip", send_coin_result))  # Команда для ручного теста

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
