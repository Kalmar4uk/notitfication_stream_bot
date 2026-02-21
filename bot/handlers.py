import requests
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import GET_STREAM_TWICH, HEADERS, USER_ID
from bot.utils import get_token_for_twich


async def hello(update: Update, context: ContextTypes):
    chat_id = update.message.chat.id
    await update.message.reply_text(f"Chat ID: {chat_id}")


async def response_stream(update: Update, context: ContextTypes):
    access_token = await get_token_for_twich()
    if access_token:
        HEADERS["Authorization"] = f"Bearer {access_token}"
        new_headres = HEADERS
        request_stream = requests.get(GET_STREAM_TWICH.format(USER_ID), headers=new_headres).json()
        if request_stream:
            result = (
                f"Начался стрим!\n"
                f"<b>{request_stream['data'][0]['title']}</b>\n"
                f"Играем в <b>{request_stream['data'][0]['game_name']}</b>\n"
                f"Начался в <b>{request_stream['data'][0]['started_at']}</b>"
            )
            photo = request_stream['data'][0]['thumbnail_url'].replace('{width}x{height}', '1960x1080')
            await update.message.reply_photo(photo, result)
        else:
            await update.message.reply_text("Что-то пошло по пизде")
    else:
        await update.message.reply_text("Что-то пошло по пизде")
