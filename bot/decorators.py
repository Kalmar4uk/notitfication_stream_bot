import requests

from bot.constants import CLIENT_ID, GET_TOKEN_TWICH, GRANT_TYPE, SECRET_KEY
from bot.exceptions import NotValidСredentials


def get_token(func):
    async def wrapper(*args, **kwargs):
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
        return await func(token_response, *args, **kwargs)
    return wrapper
