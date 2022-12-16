from pytz import timezone

from typing import Optional, List
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from models.user_model import UserModel
from core.configs import settings
from core.security import verificar_senha

from pydantic import EmailStr

# CRIAR UM ENDPOINT PARA AUTENTICAÇÃO
oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
)

async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> Optional[UserModel]:
    """RETORNAR UM USUARIO"""
    async with db as session:
        query = select(UserModel).filter(UserModel.email == email)
        result = await session.execute(query)
        usuario: UserModel = result.scalars().unique().one_or_none()

        if not usuario:
            return None
        
        if not verificar_senha(senha, usuario.password):
            return None

        return usuario

def criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    # demais informações sobre payload
    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    payload = {}

    sp = timezone('America/Sao_Paulo')
    expira = datetime.now(tz=sp) + tempo_vida
    # Prazo de expiração, a partir de agora à uma semana

    payload["type"] = tipo_token # tipo de token

    payload["exp"] = expira # quando foi criado

    payload["iat"] = datetime.now(tz=sp) # Quando foi criado

    payload["sub"] = str(sub) # identificação do usuario

    # retorna as informações codificadas
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def criar_token_acesso(sub: str) -> str:
    """
    Para demais informações
    https://jwt.io
    """
    return criar_token(
        tipo_token='access_token',
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )