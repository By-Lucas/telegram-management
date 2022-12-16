from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings


class TelegramUserModel(settings.DBBaseModel):
    __tablename__ = 'telegram_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(256))
    telegram_id = Column(Integer)
    url_fonte = Column(String(256))
    user_id = Column(Integer, ForeignKey('user.id'))
    info_user = relationship("UserModel", back_populates='info_telegram_user', lazy='joined')


class TelegramGroupsModel(settings.DBBaseModel):
    __tablename__ = 'telegram_groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    group_title = Column(String(256))
    group_username = Column(String(256))
    group_id = Column(String(256))
    group_hash = Column(String(256))
    group_admin = Column(String(256))
    info_user = relationship("UserModel", back_populates='telegram_groups', lazy='joined')

