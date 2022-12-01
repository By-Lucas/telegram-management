from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from core.send_email import SendEmail
from telegram.telegram_bot import TelegramBot
import asyncio



router = APIRouter()
send_email = SendEmail()

telegram = TelegramBot()

class TelegramApi:
   
# GET usuario Logado
    @router.get('/', status_code=status.HTTP_200_OK)
    async def telegram_groups():
        authorization =  await telegram.authorization()

        data = dict()
        groups_list = []
        
        groups = await telegram._all_groups()
        for g in groups:
            data['name'] = g.title
            data['id'] = g.id
            data['access_hash'] = g.access_hash
            groups_list.append(data.copy())


        return groups_list