from typing import Optional
from typing import List

from pydantic import BaseModel, EmailStr


class TelegramSchemaBase(BaseModel):
    id: Optional[int] = None
    username: str
    telegram_id: int
    url_fonte: str

    class Config:
        orm_mode = True


class TelegramGroupSchema(TelegramSchemaBase):
    id: Optional[int] = None
    group_title: str
    group_username: str
    group_id: int
    group_hash: str
    group_admin: str