from dotenv import load_dotenv
import os

load_dotenv(os.getcwd() + '\\.env', encoding='utf-8')


class Config:

    def __init__(self) -> None:
        # config = configparser.ConfigParser()
        # config.read('settings\\config.ini', encoding='utf-8')

        self.bot_name = os.getenv('name_bot')
        self.api_id = os.getenv('api_id')
        self.api_hash = os.getenv('api_hash')
        self.phone = os.getenv('phone')
        self.bot_token = os.getenv('bot_token')
        self.telegram_password = os.getenv('telegram_password')
        self.telegram_support = os.getenv('telegram_support')


class Message:

    def __init__(self) -> None:

        self.active = 'Usuário está ativo'
        self.waiting = 'Aguardando aprovação do usuário'
        self.disabled =  'Usuário está desativao'