from pydantic_settings import BaseSettings
from core.models.config_db import db_host, db_port, db_name, db_password, db_username



class Settings(BaseSettings):
    port: str = db_port
    host: str = db_host
    name: str = db_name
    password: str = db_password
    user: str = db_username


settings = Settings()























#     # СОЗДАЕМ ПАРАМЕТРЫ ДЛЯ ПОДКЛЮЧЕНИЯ К БД
# class Setting(BaseSettings):
#     db_url: str = 'sqlite+aiosqlite:///./all_users.db'
#     #db_echo: bool = False
#     db_echo: bool = True
#
# settings = Setting()

