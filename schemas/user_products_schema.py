from typing import Optional
from typing import List

from pydantic import BaseModel, EmailStr


class ProductSchemaBase(BaseModel):
    id: Optional[int] = None
    product_id: str
    product_name: str
    product_creator: str
    product_value: str
    status: str
    email: EmailStr
    is_admin: bool = False

    class Config:
        orm_mode = True


class  ProductSchemaUpdate(ProductSchemaBase):
    product_id: Optional[str]
    product_name: Optional[str]
    product_creator: Optional[str]
    product_value: Optional[str]
    status: Optional[str]
    email: Optional[EmailStr]
    is_admin: Optional[bool]


