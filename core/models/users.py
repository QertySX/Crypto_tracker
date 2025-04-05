from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column


# СОЗДАЕМ ТАБЛИЦУ В БД

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "all_users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    mail = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

