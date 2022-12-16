from sqlalchemy import Integer, String, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings


class ProductsModel(settings.DBBaseModel):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    product_id = Column(Integer, index=True, nullable=False, unique=True)
    product_name = Column(String(256), nullable=True)
    product_creator = Column(String(256), nullable=True)
    product_value = Column(String(10), nullable=True)
    status = Column(String(256), nullable=True)
    is_admin = Column(Boolean, default=False)
    info_user = relationship("UserModel", back_populates='info_products', lazy='joined')
