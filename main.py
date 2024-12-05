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
import asyncio  # Для добавления задержки

# Настройка логирования
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# URL для заблюренных изображений
YES_IMAGE = "https://nklk.ru/dll_image/4738.png"  # Замените на URL заблюренной картинки "Да"
NO_IMAGE = "https://nklk.ru/dll_image/4739.png"   # Замените на URL заблюренной картинки "Нет"

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
                ),  # Сообщение при отправке
            )
        ]

        await update.inline_query.answer(results, cache_time=0)
    except Exception as e:
        logger.error(f"Ошибка при обработке inline-запроса: {e}")
        await update.inline_query.answer([])  # Отправляем пустой ответ в случае ошибки

async def handle_result(update: Update, context: CallbackContext):
    """Обновление сообщения с результатом"""
    try:
        # Задержка перед обновлением результата
        await asyncio.sleep(2)  # Задержка в 2 секунды

        # Результат подбрасывания монетки
        result = random.choice(["yes", "no"])
        image_url = YES_IMAGE if result == "yes" else NO_IMAGE
        title = "Да" if result == "yes" else "Нет"

        # Обновляем сообщение с изображением и результатом
        await update.effective_message.edit_media(
            media=InputMediaPhoto(media=image_url, caption=f"<b>Монетка говорит:</b> {title}!", parse_mode="HTML")
        )
    except Exception as e:
        logger.error(f"Ошибка при обновлении сообщения: {e}")

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

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
