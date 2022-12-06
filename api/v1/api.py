from fastapi import APIRouter

from api.v1.endpoints import telegram_api
from api.v1.endpoints import edduz_api
from api.v1.endpoints import braip_api


api_router = APIRouter()

api_router.include_router(telegram_api.router, prefix='/telegram', tags=['Telegram'])
api_router.include_router(edduz_api.router, prefix='/eduzz', tags=['Eduzz'])
api_router.include_router(braip_api.router, prefix='/braip', tags=['Braip'])