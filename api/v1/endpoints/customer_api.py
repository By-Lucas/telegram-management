from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from core.send_email import SendEmail
from telegram.telegram_bot import TelegramBot
from core.plataforms.edduz import Eduzz
from telethon.tl.types import UserStatusRecently, ChatPhoto

from typing import Optional, Union
import json
import os

router = APIRouter()
send_email = SendEmail()
#telegram = TelegramBot()


def auth_eduzz():
    edduz_email = os.getenv('edduz_email')
    api_key = os.getenv('edduz_public_key')
    publick_key = os.getenv('edduz_api_key')
    edduz = Eduzz(edduz_email, api_key, publick_key)
    return edduz


class CostumerEndpoints:

    # GET status list
    @router.get('/', status_code=status.HTTP_200_OK)
    async def check_channel():
        data = {
            'client': 'Lucas Silva',
            'status': 'ativo',
            'email': 'https://t.me/blazer_space_ia',
            'phone': 'https://t.me/tk_milionario',
            'site': 'https://t.me/tk_milionario',
            'detail_product': [
                {
                    'id_product': 641639,
                    'title_product': 'TK Binary Mensal',
                    'channel_telegram': 'https://t.me/blazer_space_ia',
                    'value_product': 100.00,
                    'quantity_member': 100,
                },
                {
                    'id_product': 646927,
                    'title_product': 'TK Milionario Vitalicio',
                    'channel_telegram': 'https://t.me/blazer_space_ia',
                    'value_product': 600.00,
                    'quantity_member': 100,
                }
            ]
        }
        return data

    
    # GET status list
    @router.post('/', status_code=status.HTTP_200_OK)
    async def post_costume():
        data = {
            'client': 'Lucas Silva',
            'status': 'ativo',
            'email': 'https://t.me/blazer_space_ia',
            'phone': 'https://t.me/tk_milionario',
            'site': 'https://t.me/tk_milionario',
            'detail_product': [{
                    'id_product': 641639,
                    'title_product': 'TK Binary Mensal',
                    'channel_telegram': 'https://t.me/blazer_space_ia',
                    'value_product': 100.00,
                    'quantity_member': 100,
                },
                {
                    'id_product': 646927,
                    'title_product': 'TK Milionario Vitalicio',
                    'channel_telegram': 'https://t.me/blazer_space_ia',
                    'value_product': 600.00,
                    'quantity_member': 100,
                }
                ]
            }
        return data

    
