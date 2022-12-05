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


class EduzzEndpoints:

    # GET status list
    @router.get('/status_list', status_code=status.HTTP_200_OK)
    async def status_list():
        
        try:
            edduz = auth_eduzz()
            status_list = await edduz.status_list()
            
            return status_list

        except Exception as e:
            raise HTTPException(detail=f'Ocorreu o erro: {e}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    # GET sale list
    @router.get('/get_sale_list', status_code=status.HTTP_200_OK)
    async def get_sale_list(start_date, end_date, page=None, contract_id=None, affiliate_id=None,
                      content_id=None, invoice_status=None, client_email=None,
                      client_document=None, date_type=None):
        '''formart of start_date and end_date: 2022-12-03'''
        
        try:
            edduz = auth_eduzz()
            sale_list = await edduz.get_sale_list(start_date, end_date, page, contract_id, affiliate_id,
                      content_id, invoice_status, client_email,
                      client_document, date_type)
            
            return sale_list

        except Exception as e:
            raise HTTPException(detail=f'Ocorreu o erro: {e}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    # GET contract list
    @router.get('/get_contract_list', status_code=status.HTTP_200_OK)
    async def get_contract_list(start_date, end_date, page=None):
        '''formart of start_date and end_date: 2022-12-03'''
        
        try:
            edduz = auth_eduzz()
            contract_list = await edduz.get_contract_list(start_date=start_date, end_date=end_date, page=page)
            
            return contract_list

        except Exception as e:
            raise HTTPException(detail=f'Ocorreu o erro: {e}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    @router.get('/get_total')
    async def get_total(start_date=None, end_date=None):
        try:
            edduz = auth_eduzz()
            contract_list = await edduz.get_total(start_date=start_date, end_date=end_date)
            
            return contract_list

        except Exception as e:
            raise HTTPException(detail=f'Ocorreu o erro: {e}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    @router.get('/get_balance')
    async def get_balance():
        try:
            edduz = auth_eduzz()
            contract_list = await edduz.get_balance()
            
            return contract_list

        except Exception as e:
            raise HTTPException(detail=f'Ocorreu o erro: {e}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    @router.get('/content_list')
    async def content_list(page:int=None, active:int=None):
        try:
            edduz = auth_eduzz()
            contract_list = await edduz.content_list(page=page, active=active)
            
            return contract_list

        except Exception as e:
            raise HTTPException(detail=f'Ocorreu o erro: {e}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @router.get('/get_content/{content_id}')
    async def get_content(content_id:int):
        try:
            edduz = auth_eduzz()
            contract_list = await edduz.get_content(content_id=content_id)
            
            return contract_list

        except Exception as e:
            raise HTTPException(detail=f'Ocorreu o erro: {e}', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)