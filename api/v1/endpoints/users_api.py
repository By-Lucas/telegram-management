from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.user_model import UserModel
from models.user_telegram_model import TelegramGroupsModel, TelegramUserModel
from schemas.user_schema import TelegramSchemaBase, TelegramGroupSchema
from schemas.user_schema import (UserSchemaTelegram, 
                                UserSchemaBase,
                                UserSchemaCreate,
                                UserSchemaUpdate,
                                UserSchemaProduct,
                                UserSchemaTelegramGroup,
                                )

from core.deps import get_current_user, get_session
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso

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

    # GET usuario Logado
    @router.get('/logged', response_model=UserSchemaBase)
    def get_loged(logged_user: UserModel = Depends(get_current_user)):
        return logged_user


    # POST / Singup
    @router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
    async def post_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
        
        novo_usuario: UserModel = UserModel(id=user.id, full_name=user.full_name, birth_date=user.birth_date, 
                                            phone=user.phone,
                                            cpf=user.cpf, email=user.email, 
                                            password=gerar_hash_senha(user.password), 
                                            is_admin=user.is_admin,
                                        )
        async with db as session:
            try:
                session.add(novo_usuario)
                await session.commit()

                msg = f'Seu cadastro foi efetudo com sucesso, Faça seu login na pagina: https://xcapitalbank.com.br/trade/app/\nSeu email: {user.email} e senha: {user.password}'
                
                # send_email.enviar_email(email=user.email, 
                #                         title_email='Cadastro efetuado com sucesso...', 
                #                         body=msg
                #                         )
                return novo_usuario
            except IntegrityError:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                    detail='Já existe um usuário com este email cadastrado.')


    # GET User
    @router.get('/', response_model=List[UserSchemaBase])
    async def get_user(db: AsyncSession = Depends(get_session)):
        async with db as session:
            query = select(UserModel)
            result = await session.execute(query)
            usuarios: List[UserSchemaBase] = result.scalars().unique().all()

            return usuarios


    # GET usuário
    @router.get('/{user_email}', response_model=UserSchemaTelegram, status_code=status.HTTP_200_OK)
    async def get_user(user_email: str, db: AsyncSession = Depends(get_session)):
        async with db as session:
            query = select(UserModel).filter(UserModel.email == user_email)
            result = await session.execute(query)
            user: UserSchemaTelegram = result.scalars().unique().one_or_none()

            if user:
                return user
            else:
                raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)

        
    # UPDATE usuário
    @router.put('/{user_id}', response_model=UserSchemaBase, status_code=status.HTTP_202_ACCEPTED)
    async def update_user(usuario_id: int, usuario: UserSchemaUpdate, db: AsyncSession = Depends(get_session)):
        async with db as session:
            query = select(UserModel).filter(UserModel.id == usuario_id)
            result = await session.execute(query)
            usuario_update: UserSchemaBase = result.scalars().unique().one_or_none()

            if usuario_update:
                if usuario.nome_completo:
                    usuario_update.nome_completo = usuario.nome_completo
                if usuario.data_nascimento:
                    usuario_update.data_nascimento = usuario.data_nascimento
                if usuario.telefone:
                    usuario_update.telefone = usuario.telefone
                if usuario.cpf:
                    usuario_update.cpf = usuario.cpf
                if usuario.email:
                    usuario_update.email = usuario.email
                if usuario.eh_admin:
                    usuario_update.eh_admin = usuario.eh_admin
                if usuario.senha:
                    usuario_update.senha = gerar_hash_senha(usuario.senha)
                
                await session.commit()

                return usuario_update
            else:
                raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


    # DELETE usuário
    @router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
    async def delete_user(usuario_id: int, usuario: UserSchemaUpdate, db: AsyncSession = Depends(get_session)):
        async with db as session:
            query = select(UserModel).filter(UserModel.id == usuario_id)
            result = await session.execute(query)
            usuario_delete: UserSchemaTelegram = result.scalars().unique().one_or_none()

            if usuario_delete:
                await session.delete(usuario_delete)
                await session.commit()

                return Response(status_code=status.HTTP_204_NO_CONTENT)
            else:
                raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)

    
    # POST / info-telegram
    @router.post('/info-telegram', status_code=status.HTTP_201_CREATED, response_model=TelegramSchemaBase)
    async def post_info_telegram(telegram: TelegramSchemaBase, db:AsyncSession = Depends(get_session)):
        print(dir(telegram.id))
        #print(user_id)

        
        add_info:TelegramUserModel= TelegramUserModel(
                                                    username=telegram.username, 
                                                    telegram_id=telegram.telegram_id, 
                                                    url_fonte=telegram.url_fonte,
                                                    user_id = telegram.id
                                                )
        async with db as session:
            try:
                session.add(add_info)
                await session.commit()

                return add_info

            except IntegrityError:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Já existe um usuário com este esses dados cadastrado.')
    
    # GET telegram
    @router.get('/telegram', response_model=List[TelegramSchemaBase])
    async def get_telegram(db: AsyncSession = Depends(get_session)):
        async with db as session:
            query = select(TelegramUserModel)
            result = await session.execute(query)
            usuarios: List[TelegramSchemaBase] = result.scalars().unique().all()

            return usuarios