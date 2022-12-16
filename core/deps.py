from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from core.database import Session
from core.auth import oauth2_schema
from core.configs import settings
from models.user_model import UserModel


class TokenData(BaseModel):
    username: Optional[str] = None


async def get_session() -> Generator:
    session: AsyncSession = Session()

    try:
        yield session
    finally:
        await session.close()


async def get_current_user(db: Session = Depends(get_session),
                            token: str = Depends(oauth2_schema)) -> UserModel:
    
    #Exceção criada para facilitar o usao abaixo
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Não foi possivel autenticar a credencial',
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        # decodificar token e pegar informação do usuario logado
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )

        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        
        token_data: TokenData = TokenData(username=username)
    
    except JWTError:
        raise credential_exception
    
    async with db as session:
        query = select(UserModel).filter(UserModel.id == int(token_data.username))
        result =  await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if user is None:
            raise credential_exception

        return user