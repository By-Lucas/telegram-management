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



router = APIRouter()
send_email = SendEmail()

telegram = TelegramBot()


class TelegramApi:
   
    # GET all groups telegram
    @router.get('/', status_code=status.HTTP_200_OK)
    async def telegram_groups():
        try:
            authorization =  await telegram.authorization()
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


    # GET group telegram
    @router.get('/{user_id}', status_code=status.HTTP_200_OK)
    async def telegram_group(user_id:int):
        authorization =  await telegram.authorization()

        data = dict()
        group_info = []
        
        datas = await telegram.select_group(one_group= True, group= user_id)
        
        return json.dumps(datas.to_json())