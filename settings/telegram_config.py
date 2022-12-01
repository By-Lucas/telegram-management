from dotenv import load_dotenv
import os

load_dotenv(os.getcwd() + '\\.env', encoding='utf-8')


class Config:

    def __init__(self) -> None:
        # config = configparser.ConfigParser()
        # config.read('settings\\config.ini', encoding='utf-8')

        self.bot_name = os.environ['name_bot']
        self.api_id = os.environ['api_id']
        self.api_hash = os.environ['api_hash']
        self.phone = os.environ['phone']
        self.bot_token = os.environ['bot_token']
        self.telegram_password = os.environ['telegram_password']
        self.telegram_support = os.environ['telegram_support']


class Message:

    def __init__(self) -> None:

        self.active = 'Usuário está ativo'
        self.waiting = 'Aguardando aprovação do usuário'
        self.disabled =  'Usuário está desativao'