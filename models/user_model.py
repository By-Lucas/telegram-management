from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship

from models.user_products_model import ProductsModel
from models.user_telegram_model import TelegramGroupsModel, TelegramUserModel

from core.configs import settings


class UserModel(settings.DBBaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(256), nullable=True)
    birth_date = Column(String(256), nullable=True)
    phone = Column(String(256), nullable=True)
    cpf = Column(String(256), nullable=True)
    email = Column(String(256), index=True, nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    is_admin = Column(Boolean, default=False)

    info_products = relationship(ProductsModel, 
                                    cascade="all,delete-orphan", 
                                    back_populates='info_user', 
                                    lazy='joined', 
                                    uselist=True
                                )
    telegram_groups = relationship(TelegramGroupsModel,
                                    cascade="all,delete-orphan", 
                                    back_populates='info_user', 
                                    lazy='joined', 
                                    uselist=True
                                )
    info_telegram_user = relationship(TelegramUserModel, 
                                    cascade="all,delete-orphan",
                                    back_populates="info_user",
                                    lazy='joined', 
                                    uselist=True
                                )