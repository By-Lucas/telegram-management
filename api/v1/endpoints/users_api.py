from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from core.send_email import SendEmail
from telegram.telegram_bot import TelegramBot

from typing import Optional, Union
import json
import base64
import asyncio

router = APIRouter()
send_email = SendEmail()
telegram = TelegramBot()


class User:

    @router.get('/all-users')
    def all_users():
        data = [
            {
                'name': 'Monica liborio',
                'data': '20/10/2022',
                'status': 'Ativo'
            },
            {
                'name': 'Lucas Silva',
                'data': '20/10/2022',
                'status': 'Cancelado'
            },
            {
                'name': 'Carlos Bispo',
                'data': '20/10/2022',
                'status': 'ativa'
            },
            {
                'name': 'Joao Carlos',
                'data': '20/10/2022',
                'status': 'Desativado'
            },
            {
                'name': 'Jeferson Fernandes',
                'data': '20/10/2022',
                'status': 'Cancelado'
            },
        ]

        return data

    @router.get('/allowed-clients')
    def all_clients():
        data = dict()
        data['client_id'] = 5684523579
        data['name'] = 'Lucas Silva'
        data['status'] = 'ativo'
        data['number'] = '74981199190'
        data['group_telegram'] = 'tk binary'
        data['grorp_id'] = 1234567890
        data['products'] = [
            {
                'name': 'indicador',
                'product_id': 123456,
            },
            {
                'name': 'B3',
                'product_id': 333333,
            },
            {
                'name': 'Forex',
                'product_id': 457814,
            },
        ]


        return data