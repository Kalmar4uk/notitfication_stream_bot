import os

from dotenv import load_dotenv

load_dotenv()

TOKEN_BOT = os.getenv("TOKEN_BOT")
CLIENT_ID = os.getenv("CLIENT_ID")
SECRET_KEY = os.getenv("SECRET_KEY")
LOGIN = os.getenv("LOGIN")
USER_ID = os.getenv("USER_ID")
MY_CHAT = os.getenv("MY_CHAT")

HEADERS = {"Client-Id": f"{CLIENT_ID}", "Authorization": "Bearer {}"}
GRANT_TYPE = "client_credentials"

URL_CHANNEL = "https://www.twitch.tv/{}".format(LOGIN)
GET_TOKEN_TWICH = "https://id.twitch.tv/oauth2/token"
GET_USER_TWICH = "https://api.twitch.tv/helix/users?login={}"
GET_SCHEDULER_CHANNEL = (
    "https://api.twitch.tv/helix/schedule?broadcaster_id={}"
)
GET_STREAM_TWICH = "https://api.twitch.tv/helix/streams?user_id={}"
GET_VIDEOS_TWICH = "https://api.twitch.tv/helix/videos?user_id={}"
