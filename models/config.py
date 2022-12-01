import configparser


class Config:

    def __init__(self) -> None:

        config = configparser.ConfigParser()
        config.read('settings\\config.ini', encoding='utf-8')

        self.name = config.get("bot", "name")
        self.api_id = config.get("bot", "api_id")
        self.api_hash = config.get("bot", "api_hash")
        self.phone = config.get("bot", "phone")
        self.bot_token = config.get("bot", "bot_token")
        self.password = config.get("bot", "password")


class Message:

    def __init__(self) -> None:

        self.active = 'Usuário está ativo'
        self.waiting = 'Aguardando aprovação do usuário'
        self.disabled =  'Usuário está desativao'