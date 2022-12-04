from telethon.sync import TelegramClient
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, UserStatusRecently, ChatBannedRights, InputPeerUser

from telethon.errors.rpcerrorlist import (
    PhoneNumberBannedError, SessionPasswordNeededError,
    PasswordHashInvalidError, PhonePasswordFloodError,
    AuthKeyUnregisteredError)

from pyrogram import Client
from datetime import datetime, timedelta

from loguru import logger

import sys
import json
import os
import asyncio
from typing import Union

sys.path.append(os.path.join(os.getcwd()))

from settings.telegram_config import Config

logger.add("logs/info.log", serialize=False)
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", backtrace=True,
           diagnose=True)
logger.opt(colors=True)


class TelegramBot(Config):

    def __init__(self) -> None:
        super().__init__()

        self.client = TelegramClient(f'telegram\\sessions\\{self.phone}', self.api_id, self.api_hash)
        # self.authorization()

        # Connection with Pyrogram
        self.app = Client(
            name=self.bot_name,
            api_id=self.api_id,
            api_hash=self.api_hash,
            bot_token=self.bot_token,
            password=self.telegram_password
        )

    async def start(self):
        try:
            start = await self.app.start()
            logger.info('Pyrogram iniciado')

        except ConnectionError:
            self.app.start()
            logger.info('Pyrogram parado')

    async def authorization(self):
        '''Conexão e autorização'''
        await self.client.connect()
        if not await self.client.is_user_authorized():
            try:
                await self.client.send_code_request(self.phone)
                await self.client.sign_in(self.phone, input('Digite o código: '))

            except SessionPasswordNeededError:
                await self.client.sign_in(password=self.telegram_password)

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

    async def _all_groups(self):
        ''' (grups_permitted) Buscar apenas para grupos permitidos ou para buscar todos os grupos'''

        chats = []
        last_date = None
        chunk_size = 200
        groups = []
        all_groups = []

        result = await self.client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash=0
        ))

        chats.extend(result.chats)

        for chat in chats:
            try:
                if chat.megagroup == True:
                    groups.append(chat)
            except:
                continue

        return groups

    async def select_group(self, one_group: bool, group: int):
        '''Listar todos os grupos ou um grupo em especifico'''

        groups_all = await self._all_groups()

        i = 0
        for g in groups_all:
            groups_ = f'{str(i)}- {g.title} - {g.id}'
            # print(groups_)
            i += 1

        if one_group:
            groups_all = groups_all[group]

            return groups_all

        else:
            return groups_all

    def save_users(self, f, user):
        '''Salvar os usuários num arquivo json'''
        users = []
        json_users = {}

        json_users['username'] = user.username
        json_users['id'] = user.id
        json_users['access_hash'] = user.access_hash
        json_users['name'] = u'{}'.format(user.first_name)
        users.append(json_users.copy())
        json.dump(users, f, indent=2, ensure_ascii=False)

        return json_users

    async def _all_partifipants(self, recents_users: bool, save_users: bool, group):
        '''Listar todos os participantes'''
        # target_group = self.select_group(one_group= True)

        all_participants = []
        all_participants = await self.client.get_participants(group)

        n = 0
        users_active = []

        with open(os.path.join(os.getcwd(), f'captured_user_json/{group.title}.json'), 'w+', encoding='utf-8') as f:
            for user in all_participants:
                accept = True

                if recents_users:
                    if not user.status == UserStatusRecently():
                        accept = False

                    if accept:
                        # print(n, user.username,' - ', user.id )
                        users_active.append(user)
                        n += 1

                        if save_users:
                            self.save_users(f, user)

                else:
                    print(n, user.username, ' - ', user.id)
                    users_active.append(user)
                    n += 1

                    if save_users:
                        self.save_users(f, user)

        f.close()
        return users_active

    async def send_message_user(self, user, message):
        '''Enviar menságem para o usuário'''
        try:
            receiver = InputPeerUser(user.id, user.access_hash)
            await self.client.send_message(receiver, message, parse_mode='html')

        except Exception as e:
            logger.error(f'Erro: {e}')

    async def remove_user(self, chat_id: int, user_id: Union[str, int], time_remove: bool, days: int):
        ''' Id do grupo -1001475740997 é adicionado -100 na frente do id, o id do usuario poder ser o username'''

        if not isinstance(chat_id, int):
            logger.error('O campo chat_id deve ser numéros inteiros, EX: -1001495540997')

        if time_remove:
            if not isinstance(days, int) or days == ' ':
                logger.error('O campo days deve ser numéros inteiros e não pode ser um campo vazio')
        else:
            days = 0

        try:
            await self.start()

            data = datetime.now() + timedelta(days=days)
            result = dict()

            if time_remove:
                # Banir membro do chat e desbanir automaticamente após o tempo informadp em (data)
                remove = await self.app.ban_chat_member(chat_id=chat_id, user_id=user_id, until_date=data)
                result['message'] = f'Usuário: {user_id} agendado para ser banido em: {data}!'

            else:
                # Banir membro do chat para sempre
                remove = await self.app.ban_chat_member(chat_id=chat_id, user_id=user_id)
                result['message'] = f'Usuário: {user_id} banido com sucesso!'

            result['banned'] = remove
            logger.success(result['message'])

            return result

        except Exception as e:
            logger.error(f'Ocorreu o seguinte erro: {e}')
            raise Exception(e)

    async def clear_chat(self):
        '''Remover do grupos os usuarios desativado'''
        import datetime

        group = await self.select_group(one_group=True)

        deleted_accounts = 0
        for user in self.client.iter_participants(group):
            if user.deleted:
                try:
                    deleted_accounts += 1
                    await self.client(EditBannedRequest(group, user, ChatBannedRights(
                        until_date=datetime.timedelta(minutes=1),
                        view_messages=True
                    )))
                except Exception as exc:
                    print(f"Falha ao expulsar uma conta excluída porque: {str(exc)}")
        if deleted_accounts:
            print(f"Foram {deleted_accounts} Contas Excluídas")
        else:
            print(f"Nenhuma conta excluída encontrada em: {group.title}")
