from typing import Optional
from typing import List

from pydantic import BaseModel, EmailStr

from schemas.user_products_schema import ProductSchemaBase
from schemas.user_telegram_schema import TelegramSchemaBase, TelegramGroupSchema


"""
Vai ser criado alguns Schemas devido ao retorno das informações,
se for pra retornar as informações do usuario cadastrado, a senha não deve ser retornada
podeque é algo especifico e seguro do usuario.
"""

class UserSchemaBase(BaseModel):
    id: Optional[int] = None
    full_name: str
    birth_date: str
    phone: str
    cpf: str
    email: EmailStr
    is_admin: bool = False

    class Config:
        orm_mode = True


class UserSchemaCreate(UserSchemaBase):
    password: str


class UserSchemaTelegram(UserSchemaBase):
    """Caso seja chamado um usuario, vai ser chamado pelo dados telegram, para
    que seja mostrado os artigos apropriado pelo mesmo"""
    info_products: Optional[List[ProductSchemaBase]]
    info_telegram_user: Optional[List[TelegramSchemaBase]]
    telegram_groups: Optional[List[TelegramGroupSchema]]


class UserSchemaTelegramGroup(UserSchemaBase):
    """Caso seja chamado um usuario, vai ser chamado pelo dados telegram, para
    que seja mostrado os artigos apropriado pelo mesmo"""
    telegram_groups: Optional[List[TelegramGroupSchema]]


class UserSchemaProduct(UserSchemaBase):
    """Caso seja chamado um usuario, vai ser chamado pelo produto, para
    que seja mostrado os artigos apropriado pelo mesmo"""
    info_products: Optional[List[ProductSchemaBase]]


class UserSchemaUpdate(UserSchemaBase):
    full_name: Optional[str]
    brith_date: Optional[str]
    phone: Optional[int]
    cpf: Optional[int]
    email: Optional[EmailStr]
    password: Optional[str]
    is_admin: Optional[bool]

