import requests

from telegram_bot import TelegramBot


class TelegramManagement:
    def __init__(self) -> None:
        super().__init__()

        self.headers = {}


    def _requests(self, method:str, url_api:str ,data:dict):

        if method == 'GET':
            response = requests.request(method=method, url=url_api, data=data, headers=self.headers)