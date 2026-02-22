from telegram import Update
from telegram.ext import ContextTypes

from bot.exceptions import NotStreamNow, NotValidСredentials
from bot.utils import check_stream, get_last_video


async def hello(update: Update, context: ContextTypes):
    chat_id = update.message.chat.id
    await update.message.reply_text(f"Chat ID: {chat_id}")


async def response_stream(update: Update, context: ContextTypes):
    try:
        result, photo = await check_stream()
    except NotValidСredentials as e:
        await update.message.reply_text(
            f"Возникла проблема при авторизации: {str(e)}"
        )
    except NotStreamNow as e:
        await update.message.reply_text(str(e))
    else:
        await update.message.reply_photo(
            photo=photo,
            caption=result,
            parse_mode="HTML"
        )


async def response_last_video(update: Update, context: ContextTypes):
    result = await get_last_video()
    await update.message.reply_text(text=result, parse_mode="HTML")
