import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler

from bot.constants import TOKEN_BOT
from bot.handlers import hello, response_last_video, response_stream
from bot.logs_settings import logger

nest_asyncio.apply()


async def start() -> None:
    """Главная функция запусков"""
    logger.info("Начинаем инициализацию бота")

    app = ApplicationBuilder().token(TOKEN_BOT).build()

    logger.info("Запускаем хэндлеры бота")
    app.add_handler(CommandHandler("start", hello))
    app.add_handler(CommandHandler("check", response_stream))
    app.add_handler(CommandHandler("last_video", response_last_video))

    logger.info("Бот запущен")

    try:
        logger.info("Запускаем пуллинг бота")
        await app.run_polling()
    except Exception as e:
        logger.error(f"Возникла ошибка при пуллинге бота: {str(e)}")
