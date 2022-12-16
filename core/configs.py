from typing import List

from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

import asyncpg


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str =  'sqlite+aiosqlite:///core/database.db'
    #DB_URL: str = "postgresql+asyncpg://hkfaarrhzkykat:fac088c4f1dec32e0cb0596d5276beb61ae29c20cb10469b259fbd5b1302c908@ec2-44-199-143-43.compute-1.amazonaws.com:5432/d9gom64op639j"
    #DB_URL: str = "postgresql+asyncpg://postgres:123@localhost:5432/telegram" 
    DBBaseModel = declarative_base()


    # JWT_SECRET :A VARIAVEL TEM QUE SER MAIUSCULO
    JWT_SECRET: str = 'ucFPQUcQvujveXVTZpKMnwrY33xKRGPRr1D3kWl0tSQ'
    """
        Se desejar criar um token aleatorio, segui comandos abaixo no python, copiar
        e colar o token acima na variavel: JWT_SECRET
        import secrets
        token: str = secrets.token_urlsafe(32)
        token
    """

    ALGORITHM: str = 'HS256'
    ''' Tempo em minutos para expiração do token
         60 minutos * 27 horas * 7 dias => 1 semana'''
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings: Settings = Settings()