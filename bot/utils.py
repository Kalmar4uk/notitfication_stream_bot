import requests
import json

from bot.constants import (CLIENT_ID, GET_STREAM_TWICH, GET_TOKEN_TWICH,
                           GRANT_TYPE, HEADERS, SECRET_KEY, USER_ID)
from bot.exceptions import NotValidСredentials, NotStreamNow


async def get_token_for_twich() -> str:
    try:
        token_request = requests.post(
            GET_TOKEN_TWICH,
            data={
                "client_id": CLIENT_ID,
                "client_secret": SECRET_KEY,
                "grant_type": GRANT_TYPE
            }
        )
    except Exception as e:
        raise NotValidСredentials(error=str(e))

    if token_request.status_code == 200:
        token_response: str = token_request.json().get("access_token")
    else:
        raise NotValidСredentials(
            error=(
                f"status = {token_request.json().get('status')}, "
                f"message = {token_request.json().get('message')}"
            )
        )

    return token_response


async def check_stream() -> str:
    try:
        access_token = await get_token_for_twich()
    except NotValidСredentials as e:
        raise NotValidСredentials(error=str(e))

    HEADERS["Authorization"] = f"Bearer {access_token}"

    new_headres = HEADERS
    request_stream = requests.get(
        GET_STREAM_TWICH.format(USER_ID),
        headers=new_headres
    ).json().get("data")

    if not request_stream:
        raise NotStreamNow
    else:
        result = (
            f"Начался стрим!\n"
            f"<b>{request_stream['data'][0]['title']}</b>\n"
            f"Играем в <b>{request_stream['data'][0]['game_name']}</b>\n"
            f"Начался в <b>{request_stream['data'][0]['started_at']}</b>"
        )
        photo = request_stream['data'][0][
            'thumbnail_url'.format(
                width=1960, height=1080
            )
        ]
        return result, photo
