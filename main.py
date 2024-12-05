import random
import logging
import asyncio
import aiohttp
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
GIPHY_RANDOM_URL = f"https://api.giphy.com/v1/gifs/random?api_key={GIPHY_API_KEY}&tag=coin&rating=g"


async def fetch_random_gif_url():
    """Получить случайный GIF через API Giphy"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(GIPHY_RANDOM_URL) as response:
                logger.info(f"Статус ответа от Giphy: {response.status}")
                response.raise_for_status()

                data = await response.json()
                logger.info(f"Ответ от Giphy: {data}")

                if "data" in data and len(data["data"]) > 0:
                    gif_url = data["data"][0]["images"]["original"]["url"]
                    logger.info(f"Получена ссылка на GIF: {gif_url}")
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

        results = [
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="Подбросить монетку",
                input_message_content=InputTextMessageContent("Подбрасываем монетку... 🪙", parse_mode="HTML"),
            )
        ]

        await update.inline_query.answer(results, cache_time=0, is_personal=True)
    except Exception as e:
        logger.error(f"Ошибка при обработке inline-запроса: {e}")
        await update.inline_query.answer([])


async def handle_coin_flip_message(update: Update, context: CallbackContext):
    """Обрабатываем сообщение с текстом 'Подбрасываем монетку...'"""
    if update.message.text.strip() == "Подбрасываем монетку... 🪙":
        try:
            gif_url = await fetch_random_gif_url()
            if gif_url:
                await update.message.reply_animation(animation=gif_url, caption="Монетка крутится...")

            await asyncio.sleep(2)

            result = random.choice(["Да", "Нет"])
            await update.message.reply_text(f"Монетка говорит: {result}!")
        except Exception as e:
            logger.error(f"Ошибка при отправке результата: {e}")
            await update.message.reply_text("Произошла ошибка при подбрасывании монетки. Попробуйте снова.")


async def start(update: Update, context: CallbackContext):
    """Обработка команды /start"""
    await update.message.reply_text("Введи @<имя_бота>, чтобы подбросить монетку.")


def main():
    """Основная функция для запуска бота"""
    application = ApplicationBuilder().token("7919456091:AAHMc4yNQDvyh_nuTH8MdIiGM-8werbXuNE").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(InlineQueryHandler(inline_query))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_coin_flip_message))

    application.run_polling()


if __name__ == "__main__":
    main()
