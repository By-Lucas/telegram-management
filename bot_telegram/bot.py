from enum import Enum, auto
from telethon.sync import TelegramClient, events, Button
from helpers import Buttons

import requests

from dotenv import load_dotenv
import os
import json

load_dotenv('.env', encoding='utf-8')


class State(Enum):
    WAIT_ENABLE = auto()
    WAIT_DISABLE = auto()
    WAIT_START = auto()
    WAIT_MENU = auto()
    WAIT_CONFIG = auto()
    WAIT_PRODUCT_ID = auto()
    WAIT_EMAIL = auto()
    WAIT_USERNAME = auto()
    WAIT_PASSWORD = auto()
    WAIT_TOKEN = auto()
    WAIT_CONFIRM = auto()
    WAIT_ENTER_VALUE = auto()
    WAIT_STOP_GAIN = auto()
    WAIT_STOP_LOSS = auto()
    WAIT_PROTECTION_VALUE = auto()
    WAIT_MARTINGALE = auto()
    WAIT_MARTINGALE_MULTIPLIER = auto()
    WAIT_WHITE_MULTIPLIER = auto()
    WAIT_MORE_CONFIRM = auto()
    WAIT_NEW_CONFIRM = auto()
    WAIT_ADD_ITEM = auto()
    WAIT_SEQUENCE = auto()
    WAIT_COLOR = auto()
    WAIT_BLACK = auto()
    WAIT_RED = auto()
    WAIT_GERENCIAMENTO_TK = auto()
    WAIT_GERENCIAMENTO_SEQUENCIA = auto()
    WAIT_GERENCIAMENTO_QTD_WIN = auto()
    WAIT_GERENCIAMENTO_QTD_LOSS = auto()


fake_user = {
    "user": {
        "user_bot": 1234567890,
        "email": "teste123@gmail.com",
        "password": "teste123",
        "product_id": None,
        "token": None,
        "wallet": None,
    },
    "settings": {
        "account_type": "DEMO",
        "enter_type": "VALOR",
        "first_amount": 2,
        "enter_value": 2,
        "stop_gain": 100,
        "stop_loss": 30,
        "protection_hand": "NÃO",
        "protection_value": 2,
        "martingale": 2,
        "white_martingale": "NÃO",
        "martingale_multiplier": 2,
        "white_multiplier": 1.5,
        "stop_type": "VALOR",
        "white_gerenciamento_tk": "NÃO",
        "gerenciamento_tk_qtd": 3,
        "gerenciamento_tk_qtd_win": 4,
        "gerenciamento_tk_qtd_loss": 0
    },
    "variables": {
        "count_loss": 0,
        "count_win": 0,
        "count_martingale": 0,
        "profit": 0,
        "balance": 0,
        "created": 0,
        "is_gale": False
    },
    "strategies": [
        {"color": "preto", "sequence": "v,v,v"},
        {"color": "vermelho", "sequence": "p,p,p"}
    ]
}


class TelegramBot(object):

    def __init__(self):
        super(TelegramBot).__init__()
        self.bot_name = os.getenv('name_bot')
        self.api_id = os.getenv('api_id')
        self.api_hash = os.getenv('api_hash')
        self.phone = os.getenv('phone')
        self.bot_token = os.getenv('bot_token')

        self.url = os.getenv('url_base')

        self.bot = TelegramClient(f'telegram\\sessions\\{self.bot_name}', self.api_id, self.api_hash)
        self.conversation_state = {}
        self.state = State
        self.double = None

        @self.bot.on(events.NewMessage())
        async def handler(event):
            global user_dict, items_list, strategies_list
            sender = await event.get_sender()
            sender_id = sender.id
            print(sender_id)
            msg_id = event.id
            if sender_id != 5444523281:
                user_dict = fake_user #get_user(sender_id)
                buttons = Buttons.get_account_buttons(user_dict)
                more_buttons = Buttons.get_more_buttons(user_dict)

                if event.text == "🆘 Menu Inicial" or event.text == "/start":
                    self.conversation_state[sender_id] = self.state.WAIT_START
                elif event.text == "⚙️ Configurar":
                    await event.respond("__**Em que posso te ajudar???**__", buttons=Button.clear())
                    self.conversation_state[sender_id] = self.state.WAIT_CONFIG
                elif event.text == "🚀 Iniciar":
                    self.conversation_state[sender_id] = self.state.WAIT_ENABLE
                elif event.text == "⏹ Parar":
                    self.conversation_state[sender_id] = self.state.WAIT_DISABLE

                   
                state = self.conversation_state.get(sender_id)

                if state == self.state.WAIT_START:
                    sender = await event.get_sender()
                    markup = event.client.build_reply_markup(Buttons.get_start_button())
                    await event.respond(f"Olá {'**Visitante**' if not sender.username else sender.username} .\n"
                                        f"Sou o __**TK Global**__, bem vindo!!!",
                                        buttons=markup)
                    self.conversation_state[sender_id] = self.state.WAIT_MENU

                elif state == self.state.WAIT_MENU:
                    markup = event.client.build_reply_markup(Buttons.get_menu_buttons())
                    await event.respond("__**Insira o email utilizado na plataforma e insira também o ID do produto que comprou, o ID do contrato foi informado no seu email e na instrução da compra do produto**__")
                    await event.respond("__**Em que posso te ajudar???**__", buttons=buttons)

                elif state == self.state.WAIT_EMAIL:
                    user_dict["user"]["email"] = event.text
                    buttons[0][0].text = f"Email = {event.text}"
                    await event.respond("__**Email alterado com sucesso!!!**__", buttons=buttons)

                elif state == self.state.WAIT_PRODUCT_ID:
                    user_dict["user"]["product_id"] = event.text
                    buttons[1][0].text = f"Produto ID: = {event.text}"
                    await event.respond("__**ID do contrato alterada com sucesso!!!**__", buttons=buttons)
             

                elif state == self.state.WAIT_CONFIG:
                    #markup = event.client.build_reply_markup(Buttons.get_menu_buttons())
                    await event.respond("__**Validando informações...**__", buttons=buttons)
                    #await self.bot.delete_messages(event.sender_id, [msg_id])

                elif state == self.state.WAIT_CONFIRM:
                    del self.conversation_state[sender_id]
                    #self.conversation_state[sender_id] = self.state.WAIT_START
                    
                

        @self.bot.on(events.CallbackQuery())
        async def call_handler(event):
            global user_dict, items_list, strategies_list
            selected = event.data.decode('utf-8')
            msg_id = event.query.msg_id
            sender = await event.get_sender()
            sender_id = sender.id
            user_dict = fake_user #get_user(sender_id)
            buttons_name = [button_name for button_name in user_dict["settings"]]
            buttons = Buttons.get_account_buttons(user_dict)
            more_buttons = Buttons.get_more_buttons(user_dict)
            strategy_buttons = Buttons.get_strategy_buttons(user_dict)

            print(selected)

            if selected.lower() == "MORE":
                await event.respond("__**Configurações Gerais**__", buttons=more_buttons)
                await self.bot.delete_messages(event.sender_id, [msg_id])
            
            elif selected.upper() == "PRODUCT_ID":
                await event.respond("__**Entre com o ID do produto**__")
                await self.bot.delete_messages(sender_id, [msg_id])
                self.conversation_state[sender_id] = self.state.WAIT_PRODUCT_ID

            elif selected.upper() == "EMAIL":
                await event.respond(f"__**Entre com o email da plataforma**__")
                await self.bot.delete_messages(sender_id, [msg_id])
                self.conversation_state[sender_id] = self.state.WAIT_EMAIL
            
            elif selected.upper() == "CONFIRMAR":
                await event.respond(f"__**Aguarde um momento, estamos verificando as informações...**__")
                await self.bot.delete_messages(sender_id, [msg_id])
                self.conversation_state[sender_id] = self.state.WAIT_ENABLE

                validation = self.user_verification(int(user_dict["user"]["product_id"]), user_dict["user"]["email"])

                if validation is not None:

                    if validation['data'][0]['sale_status'] > 1:

                        await self.bot.delete_messages(sender_id, [msg_id])
                        await event.respond(f"__**Informações verificada com, você está em dia ✅**__")
                        
                        #print(validation['data'][0])

                        data = {
                            "id": sender.id,
                            "full_name": validation['data'][0]['client_name'],
                            "birth_date": validation['data'][0]['due_date'],
                            "phone": validation['data'][0]['client_cel'],
                            "cpf": sender.id, #validation['data'][0]['client_document'] ,
                            "email": validation['data'][0]['client_email'],
                            "is_admin": False,
                            "password": sender.id
                        }

                        add_user = self.new_user(data=data)

                        if add_user.status_code == 201:
                            params = {
                                    "username": sender.username,
                                    "telegram_id": sender.id,
                                    "url_fonte": f"https://t.me/{sender.username}",
                                    "id": sender.id
                                }

                            add_info = self.add_info_telegram(data=params)

                            await event.respond(f"__**Nome completo: {validation['data'][0]['client_name']}**__")
                            await event.respond(f"__**Status: {validation['data'][0]['sale_status_name']}**__")
                            await event.respond(f"__**Valor: {validation['data'][0]['sale_total']}**__")
                            await event.respond(f"__**Produto: {validation['data'][0]['content_title']}**__")
                            await event.respond(f"__**Vencimento: {validation['data'][0]['due_date']}**__")

                            self.conversation_state[sender_id] = self.state.WAIT_START
                    
                    else:

                        await event.respond(f"__**Informações verificada com, você está não em dia ⛔️**__")
                        await event.respond(f"__**Nome completo: {validation['data'][0]['client_name']}**__")
                        await event.respond(f"__**Status: {validation['data'][0]['sale_status_name']}**__")
                        await event.respond(f"__**Valor: {validation['data'][0]['sale_total']}**__")
                        await event.respond(f"__**Produto: {validation['data'][0]['content_title']}**__")
                        await event.respond(f"__**Vencimento: {validation['data'][0]['due_date']}**__")

                        self.conversation_state[sender_id] = self.state.WAIT_START
                
                else:
                    await event.respond(f"__**Houve um erro interno, entre em contato com o administrador**__")
                    self.conversation_state[sender_id] = self.state.WAIT_START
                    
            elif selected.upper() == "VOLTAR":
                await self.bot.delete_messages(sender_id, [msg_id])
                self.conversation_state[sender_id] = self.state.WAIT_START


    def search_info_group(self, id):
        try:
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request('POST', url=f'{self.url}/user/info-telegram',data=json.dumps(data), headers=headers)
            return response

        except Exception as e:
            print(e)
                
    
    def add_info_telegram(self, data):
        try:
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request('POST', url=f'{self.url}/user/info-telegram',data=json.dumps(data), headers=headers)
            return response

        except Exception as e:
            print(e)

    
    def new_user(self, data):
        try:
            headers = {
                'Content-Type': 'application/json'
            }
       
            response = requests.request('POST', url=f'{self.url}/user/signup', data=json.dumps(data), headers=headers)
            return response

        except Exception as e:
            print(e)



    def get_user(self, email:str):
        headers = {
                'Content-Type': 'application/json'
        }

        response = requests.request('GET', url=f'{self.url}/user/{email}', headers=headers)

        if response.status_code == 200:
            return response.json()


    def user_verification(self, contracti_id:int, email:str) -> None:
        data = {
            'start_date': '2020-12-03',
            'end_date': '2021-12-03',
            'contract_id': contracti_id ,
            'client_email': email
        }

        headers = {
                'Content-Type': 'application/json'
        }

        response = requests.request('GET', url=f'{self.url}/eduzz/get_sale_list', params=data, headers=headers)

        if response.json()['data'] != []:
            return response.json()


    def start_service(self):
        self.bot.start(bot_token=self.bot_token)
        print("Starting telegram bot!!!")
        self.bot.run_until_disconnected()


if __name__== '__main__':
    bot = TelegramBot()
    bot.start_service()