from fastapi import APIRouter

from api.v1.endpoints import telegram_api
from api.v1.endpoints import edduz_api


api_router = APIRouter()

api_router.include_router(telegram_api.router, prefix='/telegram', tags=['telegram'])
api_router.include_router(edduz_api.router, prefix='/eduzz', tags=['eduzz'])
