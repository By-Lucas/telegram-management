from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from core.send_email import SendEmail
from telegram.telegram_bot import TelegramBot
from telethon.tl.types import UserStatusRecently, ChatPhoto

from typing import Optional, Union
import json
import base64
import asyncio

router = APIRouter()
send_email = SendEmail()
telegram = TelegramBot()


class TelegramApi:

    # GET all chats telegram
    @router.get('/all-chats', status_code=status.HTTP_200_OK)
    async def telegram_groups():
        try:
            authorization = await telegram.authorization()
            data = dict()
            groups_list = []

            groups = await telegram._all_groups()
            n = 0

            for g in groups:
                data['name'] = g.title
                data['id'] = g.id
                data['access_hash'] = g.access_hash
                data['position'] = n
                groups_list.append(data.copy())

                n += 1

            return groups_list

        except Exception as e:
            raise HTTPException(detail=f'Ocorreu o erro: {e}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # GET chat telegram
    @router.get('/{chat_id}', status_code=status.HTTP_200_OK)
    async def telegram_group(chat_id: int):
        try:

            authorization = await telegram.authorization()

            group = await telegram.select_group(one_group=True, group=chat_id)
            data = group.__dict__

            if data['photo'] is not None:
                photo_base64 = base64.b64encode(data['photo'].stripped_thumb).decode()

                data['photo'] = {
                    'photo_id': data['photo'].photo_id,
                    'photo_b64encode': photo_base64
                }

            return data

        except Exception as e:
            raise HTTPException(detail=f'Ocorreu o erro: {e}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # GET all users
    @router.get('/participants/{chat_id}', status_code=status.HTTP_200_OK)
    async def telegram_participants(chat_id: int, recents_users: bool, save_users: bool):
        try:

            authorization = await telegram.authorization()

            group = await telegram.select_group(one_group=True, group=chat_id)

            all_participants = await telegram._all_partifipants(recents_users=recents_users, save_users=save_users,
                                                                group=group)

            users = []

            for user in all_participants:
                data = user.__dict__

                if data['photo'] is not None:
                    photo_base64 = base64.b64encode(data['photo'].stripped_thumb).decode()
                    data['photo'] = {
                        'photo_id': data['photo'].photo_id,
                        'photo_b64encode': photo_base64
                    }

                if data['emoji_status'] is not None:
                    data['emoji_status'] = data['emoji_status'].document_id

                if data['status'] is not None:
                    data['status'] = 'UserStatusRecently()'

                if data['participant'] is not None:
                    data['participant'] = {
                        'user_id': data['participant'].user_id,
                        'date': json.dumps(data['participant'].date, default=str)
                    }

                users.append(data.copy())

            return users

        except Exception as e:
            raise HTTPException(detail=f'Ocorreu o erro: {e}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # GET chat telegram
    @router.post('/ban-user', status_code=status.HTTP_204_NO_CONTENT)
    async def ban_user(chat_id: int, user: Union[str, int], time_remove: bool, days: int = None):
        '''
        Id do grupo EX: -1001475740997 ?? adicionado -100 na frente do id, o id do usuario poder ser somente o username,\n
        time_remove: Verifica se pretende agendar a data de banimento do usuario,\n
        days:  dias de agendamento para o banimento
        '''

        if not isinstance(chat_id, int):
            raise HTTPException(detail=f'O campo chat_id deve ser num??ros inteiros, EX: -1001495540997',
                                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if time_remove:
            if not isinstance(days, int) or days == ' ':
                raise HTTPException(
                    detail=f'O campo days deve ser num??ros inteiros e n??o pode ser um campo vazio se estiver com time_remove habilitado',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            days = 0

        try:
            authorization = await telegram.authorization()
            user_ban = await telegram.remove_user(chat_id=chat_id, user_id=user, time_remove=time_remove, days=days)

            return user_ban

        except Exception as e:
            raise HTTPException(detail=f'Ocorreu o seguinte erro: {e}',
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
