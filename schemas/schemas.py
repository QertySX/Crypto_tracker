from pydantic import BaseModel, EmailStr

# СОЗДАЕМ ВАЛИДАЦИЮ ДАННЫХ КОТОРЫЕ БУДЕМ ПОЛУЧАТЬ ОТ register_users()
class UserRegistration(BaseModel):
    username: str
    mail: str
    password: str

