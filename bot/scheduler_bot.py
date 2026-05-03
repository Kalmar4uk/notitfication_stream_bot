from telegram.ext import ApplicationBuilder
from bot.logs_settings import logger
from bot.utils import check_stream
from bot.exceptions import NotValidСredentials, NotStreamNow, ExceptionRequestTwitch
from bot.constants import MY_CHAT


async def check_scheduler_stream(app: ApplicationBuilder) -> None:
    try:
        id_stream, result, photo = await check_stream()
        if id_stream == app.bot_data.get("id_stream"):
            raise NotStreamNow()
    except NotValidСredentials as e:
        logger.error(f"Возникла проблема при авторизации: {str(e)}")
    except NotStreamNow as e:
        logger.info(str(e))
        await app.bot.send_message(
            chat_id=MY_CHAT, text=str(e)
        )
    except Exception as e:
        logger.error(str(e))
    else:
        logger.info("Отправили сообщение о текущем стриме")
        await app.bot.send_massage(
            chat_id=MY_CHAT,
            photo=photo,
            caption=result,
            parse_mode="HTML"
        )
        app.bot_data["id_stream"] = id_stream
