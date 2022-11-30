from telethon.sync import TelegramClient
from telethon import functions
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, UserStatusRecently, ChatBannedRights

from telethon.errors.rpcerrorlist import (
    PhoneNumberBannedError, SessionPasswordNeededError, 
    PasswordHashInvalidError, PhonePasswordFloodError,
    AuthKeyUnregisteredError)

from loguru import logger
import sys
import asyncio

from models.config import Config



logger.add("logs/info.log",  serialize=False)
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", backtrace=True, diagnose=True)
logger.opt(colors=True)


class TelegramBot(Config):

    def __init__(self) -> None:
        super().__init__()

        self.client = TelegramClient(f'sessions\\{self.phone}', self.api_id, self.api_hash)
        self.authorization()


    def authorization(self) -> None:
        '''Conexão e autorização'''
        self.client.connect()
        if not self.client.is_user_authorized():
            try:
                self.client.send_code_request(self.phone)
                self.client.sign_in(self.phone, input('Digite o código: '))

            except SessionPasswordNeededError:
                self.client.sign_in(password= self.password)

            except PasswordHashInvalidError:
                logger.error('Senha incorreta')
                raise Exception('Senha incorreta')

            except PhoneNumberBannedError:
                logger.error(f'O número {self.phone} está banido')
                raise Exception(f'O número {self.phone} está banido')

            except PhonePasswordFloodError:
                logger.error('Você tentou fazer login muitas vezes (causado por NoneType)')
                raise Exception('Você tentou fazer login muitas vezes (causado por NoneType)')

            except AuthKeyUnregisteredError:
                logger.error('A chave não está cadastrada no sistema (causado por GetDialogsRequest)')
                raise Exception('A chave não está cadastrada no sistema (causado por GetDialogsRequest)')
            
            except BaseException as e:
                logger.error(f'Error {e}')
                raise Exception(f'Error {e}')
                


    def _all_groups(self, groups_permitted:bool= False):
        ''' (grups_permitted) Buscar apenas para grupos permitidos ou para buscar todos os grupos'''

        chats = []
        last_date = None
        chunk_size = 200
        groups=[]
        all_groups = []

        result = self.client(GetDialogsRequest(
                    offset_date=last_date,
                    offset_id=0,
                    offset_peer=InputPeerEmpty(),
                    limit=chunk_size,
                    hash = 0
                ))

        chats.extend(result.chats)
        dialogs = self.client.get_dialogs()

        if groups_permitted:
            for chat in chats:
                try:
                    if chat.megagroup == True:
                        groups.append(chat)
                except:
                    continue
        
        else:
            for i in dialogs:
                try:
                    i.entity.status
                except:
                    groups.append(i)
                    continue

        return groups

    
    def select_group(self, one_group:bool = False):
        '''Listar todos os grupos ou um grupo em especifico'''
        groups_all = self._all_groups(groups_permitted=True)

        i = 0
        for g in groups_all:
            groups_ = f'{str(i)}- {g.title}'
            print(groups_)
            i+=1

        if one_group:
            g_index = input("Digite o número do grupo: ")
            groups_all=groups_all[int(g_index)]
            return groups_all
        
        else:
            return groups_all


    def _all_partifipants(self, user:str = None):
        '''Listar todos os participantes'''
        target_group = self.select_group(True)

        all_participants = []
        all_participants = self.client.get_participants(target_group)
        
        n=0
        users_active = []

        for user in all_participants:
            accept = True

            if not user.status == UserStatusRecently():
                accept = False

            if accept:
                print(n, user.username)
                users_active.append(user)
                n+=1
        return users_active
        

    def remove_user(self, user:list):
        '''Remover do grupos um usário especofico'''
        with TelegramClient(self.name, self.api_id, self.api_hash) as client:
            result = client(functions.contacts.DeleteContactsRequest(id=user))
            print(result.stringify())
            print('removido')


    def clear_chat(self):
        '''Remover do grupos os usuarios desativado'''
        import datetime

        group = self.select_group(True)

        deleted_accounts = 0
        for user in self.client.iter_participants(group):
            if user.deleted:
                try:
                    deleted_accounts += 1
                    self.client(EditBannedRequest(group, user, ChatBannedRights(
                    until_date=datetime.timedelta(minutes=1),
                    view_messages=True
                    )))
                except Exception as exc:
                    print(f"Falha ao expulsar uma conta excluída porque: {str(exc)}")
        if deleted_accounts:
            print(f"Foram {deleted_accounts} Contas Excluídas")
        else:
            print(f"Nenhuma conta excluída encontrada em: {group.title}")


if __name__ == '__main__':
    bot = TelegramBot()

    rr = bot.clear_chat()

    
    