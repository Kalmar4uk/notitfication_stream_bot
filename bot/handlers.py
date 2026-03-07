from telegram import Update
from telegram.ext import ContextTypes

from bot.exceptions import (ExceptionRequestTwitch, NotStreamNow,
                            NotValidСredentials)
from bot.logs_settings import logger
from bot.utils import check_stream, get_last_video


async def hello(update: Update, context: ContextTypes):
    chat_id = update.message.chat.id
    await update.message.reply_text(f"Chat ID: {chat_id}")


async def response_stream(update: Update, context: ContextTypes):
    logger.info("Получили команду запроса стрима")
    try:
        result, photo = await check_stream()
    except NotValidСredentials as e:
        logger.error(f"Возникла проблема при авторизации: {str(e)}")
        await update.message.reply_text(
            f"Возникла проблема при авторизации: {str(e)}"
        )
    except NotStreamNow as e:
        logger.info(str(e))
        await update.message.reply_text(str(e))
    except ExceptionRequestTwitch as e:
        logger.info(str(e))
        await update.message.reply_text(str(e))
    except Exception as e:
        logger.info(f"Возникла неизвестная ошибка: {str(e)}")
        await update.message.reply_text("Неизвсетная ошибка")
    else:
        logger.info("Отправили сообщение в чат")
        await update.message.reply_photo(
            photo=photo,
            caption=result,
            parse_mode="HTML"
        )


async def response_last_video(update: Update, context: ContextTypes):
    logger.info("Получили команду запроса последнего прошедшего стрима")
    result = await get_last_video()
    await update.message.reply_text(text=result, parse_mode="HTML")
