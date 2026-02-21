import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler

from bot.constants import TOKEN_BOT
from bot.handlers import response_stream, hello

nest_asyncio.apply()


async def start() -> None:
    """Главная функция запусков"""

    app = ApplicationBuilder().token(TOKEN_BOT).build()

    app.add_handler(CommandHandler("start", hello))
    app.add_handler(CommandHandler("check", response_stream))

    await app.run_polling()
