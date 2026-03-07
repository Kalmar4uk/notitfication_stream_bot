from datetime import datetime, timedelta

import requests

from bot.constants import GET_STREAM_TWICH, GET_VIDEOS_TWICH, HEADERS
from bot.decorators import get_token
from bot.exceptions import ExceptionRequestTwitch, NotStreamNow
from bot.logs_settings import logger


async def prepare_datetime_from_response_twich(date_string: str) -> datetime:
    date_string = date_string.replace("Z", "+00:00")
    utc_time = datetime.fromisoformat(date_string)
    msk_time = utc_time + timedelta(hours=3)
    return msk_time.strftime("%d.%m.%Y %H:%M")


@get_token
async def check_stream(token: str | None = None) -> tuple[str, str | None]:
    logger.info("Сохраняем новые креды")
    HEADERS["Authorization"] = f"Bearer {token}"

    new_headres = HEADERS

    logger.info("Отправляем запрос для получения стрима")
    try:
        request_stream = requests.get(
            GET_STREAM_TWICH,
            headers=new_headres
        ).json().get("data")
    except Exception as e:
        raise ExceptionRequestTwitch(error=str(e))

    if not request_stream:
        raise NotStreamNow()
    else:
        logger.info("Ответ получен, готовим сообщение для отправки в чат")
        prepare_datetime_start = await prepare_datetime_from_response_twich(
            request_stream[0].get("started_at")
        )
        result = (
            f"Начался стрим!\n\n"
            f"<b>{request_stream[0].get('title')}</b>\n"
            f"Играем в <b>{request_stream[0].get('game_name')}</b>\n"
            f"Начался <b>{prepare_datetime_start}</b>"
        )

        try:
            photo = request_stream[0].get(
                'thumbnail_url'
            ).format(
                width=1960, height=1080
            )
        except AttributeError:
            photo = None

        return result, photo


@get_token
async def get_last_video(token: str | None = None) -> str:
    logger.info("Сохраняем новые креды")
    HEADERS["Authorization"] = f"Bearer {token}"

    new_headres = HEADERS

    logger.info("Отправляем запрос для получения прошедшего стрима")
    request_video = requests.get(
        GET_VIDEOS_TWICH,
        headers=new_headres
    ).json().get("data")[0]

    logger.info("Ответ получен, готовим сообщение для отправки в чат")
    prepare_datetime_start = await prepare_datetime_from_response_twich(
        request_video.get("created_at")
    )

    result = (
        f"Прошедший недавно стрим\n\n"
        f"<b>{request_video.get('title')}</b>\n\n"
        f"Проходил <b>{prepare_datetime_start}</b>\n"
        f"Ссылка на видео {request_video.get('url')}"
    )

    return result
