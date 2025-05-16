import requests

from config.settings import TG_BOT_TOKEN


def send_tg_message(id, message):
    params = {
        "text": message,
        "chat_id": id,
    }
    return requests.get(
        f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage", params=params
    )
