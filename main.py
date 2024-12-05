import random
import logging
import asyncio
import aiohttp  # Используем асинхронную библиотеку для запросов
import uuid
from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    InlineQueryHandler,
    MessageHandler,
    filters,
    CallbackContext,
)

# Настройка логирования
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Giphy API
GIPHY_API_KEY = "ebUU78UvD6s5vr09ODs1qGdEsAvAyFfc"
GIPHY_RANDOM_URL = f"https://api.giphy.com/v1/gifs/random?api_key={GIPHY_API_KEY}&tag=money"

async def fetch_random_gif_url():
    """Получить случайный GIF через API Giphy"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(GIPHY_RANDOM_URL) as response:
                response.raise_for_status()
                data = await response.json()

                # Проверяем, что данные приходят в нужном формате
                if "data" in data and len(data["data"]) > 0:
                    gif_url = data["data"][0]["images"]["original"]["url"]
                    return gif_url
                else:
                    logger.error("Ответ от Giphy не содержит данных или пустой массив.")
                    return None
    except Exception as e:
        logger.error(f"Ошибка при запросе к Giphy API: {e}")
        return None

async def inline_query(update: Update, context: CallbackContext):
    """Обработка inline-запросов"""
    try:
        logger.info(f"Получен inline-запрос от {update.inline_query.from_user.id}")

        # Создаем инлайн-результат с текстом "Подбросить монетку"
        results = [
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),  # Уникальный идентификатор
                title="Подбросить монетку",
                input_message_content=InputTextMessageContent(
                    "Подбрасываем монетку... 🪙", parse_mode="HTML"
                ),
            )
        ]

        await update.inline_query.answer(results, cache_time=0, is_personal=True)
    except Exception as e:
        logger.error(f"Ошибка при обработке inline-запроса: {e}")
        await update.inline_query.answer([])  # Отправляем пустой ответ в случае ошибки

async def handle_coin_flip_message(update: Update, context: CallbackContext):
    """Обрабатываем сообщение с текстом 'Подбрасываем монетку...'"""
    if update.message.text == "Подбрасываем монетку... 🪙":
        try:
            # Получаем случайную GIF
            gif_url = await fetch_random_gif_url()
            if gif_url:
                # Отправляем GIF
                await update.message.reply_animation(animation=gif_url, caption="Монетка крутится...")

            # Задержка перед отправкой результата
            await asyncio.sleep(2)

            # Результат подбрасывания монетки
            result = random.choice(["Да", "Нет"])
            await update.message.reply_text(f"Монетка говорит: {result}!")
        except Exception as e:
            logger.error(f"Ошибка при отправке результата: {e}")

async def start(update: Update, context: CallbackContext):
    """Обработка команды /start"""
    await update.message.reply_text("Введи @<имя_бота>, чтобы подбросить монетку.")

def main():
    """Основная функция для запуска бота"""
    application = ApplicationBuilder().token("7919456091:AAHMc4yNQDvyh_nuTH8MdIiGM-8werbXuNE").build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(InlineQueryHandler(inline_query))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_coin_flip_message))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
