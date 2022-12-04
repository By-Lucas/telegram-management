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
import base64
import os
import asyncio

router = APIRouter()
send_email = SendEmail()
#telegram = TelegramBot()


class BraipEndpoints:

    # GET status list
    @router.get('/users', status_code=status.HTTP_200_OK)
    async def status_list():
        
        try:
            
            return {'users': 'Completar rota'}

        except Exception as e:
            raise HTTPException(detail=f'Ocorreu o erro: {e}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
