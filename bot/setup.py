import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bot.constants import TOKEN_BOT
from bot.handlers import hello, response_last_video, response_stream
from bot.logs_settings import logger
from bot.exceptions import ErrorStartSchedule
from bot.scheduler_bot import check_scheduler_stream

nest_asyncio.apply()

app = ApplicationBuilder().token(TOKEN_BOT).build()


async def setup_scheduler() -> AsyncIOScheduler:
    global app
    try:
        scheduler = AsyncIOScheduler()
        scheduler.add_job(
            check_scheduler_stream,
            trigger=IntervalTrigger(seconds=30),
            kwargs={"app": app}
        )
        scheduler.start()
    except Exception as e:
        logger.error(f"Возникла ошибка при запуске планировщика: {str(e)}")
        raise ErrorStartSchedule(
            f"Возникла ошибка при запуске планировщика: {str(e)}"
        )
    return scheduler

async def start() -> None:
    """Главная функция запусков"""
    logger.info("Запускает планировщик")
    await setup_scheduler()

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
