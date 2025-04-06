from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
import logging
from fastapi import Form
from sqlalchemy.exc import IntegrityError
from core.models.db_helper import db_helper
from get_crypto_data import process_crypto_data, get_raw_crypto_data
from schemas.schemas import UserRegistration
from core.models.users import Users


# СОЗДАНИЕ БАЗЫ ДАННЫХ
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await db_helper.create_db()
        logging.info("База данных успешно создана")
        yield
    except Exception as e:
        logging.info('Error ', e)


app = FastAPI(lifespan=lifespan)

# Для работы с html
templates = Jinja2Templates(directory="templates")


logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(),  # Вывод в консоль
        logging.FileHandler("app.log", encoding='utf-8')  # Вывод в файл
    ]
)


    # ФУНКЦИЯ КОТОРАЯ ПОЛУЧАЕТ ДАННЫЕ И ДЕЛАЕТ ВЕБ-СТРАНИЦУ
@app.get('/crypto')
async def render_crypto_page(request: Request):
    try:
        processed_data = await process_crypto_data()
        page = templates.TemplateResponse("index.html", {"request": request, "cryptos": processed_data})

        if 'error' in processed_data:
            logging.info('[INFO] Ошибка получения данных в func_3')

        else:
            return page

    except Exception as e:
        logging.info(f'Ошибка:', e)


    # ФУНКЦИЯ КОТОРАЯ ДОБАВЛЯЕТ ПОИСКОВУЮ СТРОКУ
@app.get('/search')
async def search_bar(request: Request, name_crypto: str = Query(None)):
    try:
        data = await process_crypto_data()
        
        if not name_crypto:
            return templates.TemplateResponse("crypto_list.html", {"request": request, "cryptos": data})
        
        filtered_data = dict()
        for crypto_name, crypto_data in data.items():
            if name_crypto.lower() in crypto_name.lower():
                filtered_data[crypto_name] = crypto_data
        
        if filtered_data:
            logging.info(f'[INFO] Данные в func_4 найдены! Криптовалюта: {name_crypto}')
            return templates.TemplateResponse(
                "crypto_list.html", 
                {"request": request, "cryptos": filtered_data, "search": name_crypto}
            )
        else:
            return templates.TemplateResponse(
                "crypto_list.html", 
                {"request": request, "error": f'Криптовалюта "{name_crypto}" не найдена'}
            )
    except Exception as e:
        logging.info(f'Ошибка:', e)


@app.get('/register')
async def page_register(request: Request):
    try:
        return templates.TemplateResponse('register.html', {'request': request})
    except Exception as e:
        logging.info(f'Ошибка:', e)


@app.post('/register')  # Добавлен Form, так как POST-запрос приходит не в JSON, а в html формате
async def register_user(username: str = Form(...), mail: str = Form(...), password: str = Form(...)):
    try:
        logging.debug(f"Получены данные: username={username}, mail={mail}, password={password}")

        # Преобразование Form в Pydantic модель для дальнейшей валидации данных
        user_data = UserRegistration(username=username, mail=mail, password=password)

        # Инициализируем класс Users с параметрами, полученными от пользователя
        add_user = Users(
            username=user_data.username,
            mail=user_data.mail,
            password=user_data.password
        )

        # Добавляем пользователя в сессию
        async with db_helper.session_factory() as session:
            session.add(add_user)
            logging.info(f'Пользователь {add_user.username} прошел регистрацию')
            await session.commit()
            logging.debug("Коммит выполнен")

        return {"message": f"User {add_user.username} registered successfully"}

    except IntegrityError as e:
        logging.error(f'Пользователь с таким именем или почтой уже существует: {e}')
        return {"error": "Пользователь с таким именем или почтой уже существует"}

    except Exception as e:
        logging.exception(f'Ошибка при регистрации пользователя: {e}')
        return {"error": "Ошибка при регистрации пользователя"}




if __name__ == "__main__":
    uvicorn.run("main:app", reload=False)


