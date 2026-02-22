import json
from datetime import datetime, timedelta

import requests

from bot.constants import GET_STREAM_TWICH, GET_VIDEOS_TWICH, HEADERS, USER_ID
from bot.decorators import get_token
from bot.exceptions import NotStreamNow


async def prepare_datetime_from_response_twich(date_string: str) -> datetime:
    date_string = date_string.replace("Z", "+00:00")
    utc_time = datetime.fromisoformat(date_string)
    msk_time = utc_time + timedelta(hours=3)
    return msk_time.strftime("%d.%m.%Y %H:%M")


@get_token
async def check_stream(token: str | None = None) -> tuple[str, str | None]:
    HEADERS["Authorization"] = f"Bearer {token}"

    new_headres = HEADERS

    request_stream = requests.get(
        GET_STREAM_TWICH.format(USER_ID),
        headers=new_headres
    ).json().get("data")[0]

    if not request_stream:
        raise NotStreamNow()
    else:
        prepare_datetime_start = await prepare_datetime_from_response_twich(
            request_stream.get("started_at")
        )
        result = (
            f"Начался стрим!\n\n"
            f"<b>{request_stream.get('title')}</b>\n"
            f"Играем в <b>{request_stream.get('game_name')}</b>\n"
            f"Начался <b>{prepare_datetime_start}</b>"
        )

        try:
            photo = request_stream.get(
                'thumbnail_url'
            ).format(
                width=1960, height=1080
            )
        except AttributeError:
            photo = None

        return result, photo


@get_token
async def get_last_video(token: str | None = None):
    HEADERS["Authorization"] = f"Bearer {token}"

    new_headres = HEADERS
    request_video = requests.get(
        GET_VIDEOS_TWICH.format(USER_ID),
        headers=new_headres
    ).json().get("data")[0]

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
