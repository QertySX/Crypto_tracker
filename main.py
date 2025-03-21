import aiohttp
from config import api_key
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import logging
from typing import List
from pydantic import BaseModel, EmailStr, field_validator, constr
import asyncio


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:8000']
)

templates = Jinja2Templates(directory="templates")


logging.basicConfig(level=logging.DEBUG)


class UserRegistration(BaseModel):
    username: str
    mail: EmailStr
    password: constr(min_length=8)

    # ФУНКЦИЯ ДЛЯ ЗАПРОСА API И ПОЛУЧЕНИЮ СПИСКА КРИПТОВАЛЮТ
async def get_raw_crypto_data():
    try:
        logging.info("Получение данных криптовалюты...")
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': api_key,
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:

                if response.status == 200:
                    result = await response.json()
                    logging.info("[INFO] Данные в func_1 получены!")
                    return result
                else:
                    logging.error(f'[INFO] Ошибка {response.status}' )
                    return {f"[INFO] HTTP ошибка {response.status}"}
            
    except Exception as e:
        print('[INFO] Ошибка: ', e)


    # ФУНКЦИЯ КОТОРАЯ ОБРАБАТЫВАЕТ ПОЛУЧЕННЫЕ ДАННЫЕ ИЗ 1 ФУНКЦИИ
async def process_crypto_data() -> dict:
    try:
        raw_crypto_data = await get_raw_crypto_data()
        all_data = dict()

        if 'data' not in raw_crypto_data:
            logging.error('[INFO] Данные из func_1 не получены')
            return {"error": "Данные из func_1 не получены"}
        else:
            for crypto in raw_crypto_data['data']:
                necessary_data = {
                    "price": crypto['quote']['USD']['price'],
                    "volume_24h": crypto['quote']['USD']['volume_24h'],
                    "percent_change_24h": crypto['quote']['USD']['percent_change_24h'],
                    "market_cap": crypto['quote']['USD']['market_cap']
                }
                all_data[crypto['name']] = necessary_data

        logging.info("[INFO] Данные в func_2 обработаны!")

        return all_data

    except Exception as e:
        print('[INFO] Ошибка', e)


    # ФУНКЦИЯ КОТОРАЯ ПОЛУЧАЕТ ДАННЫЕ И ДЕЛАЕТ ВЕБ-СТРАНИЦУ
@app.get('/crypto')
async def render_crypto_page(request: Request):
    try:
        processed_data = await process_crypto_data()
        page = templates.TemplateResponse("index.html", {"request": request, "cryptos": processed_data})

        if 'error' in processed_data:
            logging.error('[INFO] Ошибка получения данных в func_3')

        else:
            return page

    except Exception as e:
        print('[INFO] Ошибка', e)


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
        print('[INFO] Ошибка', e)



@app.get('/register')
async def page_register(request: Request):
    try:
        return templates.TemplateResponse('register.html', {'request': request})
    except Exception as e:
        print('[INFO] Ошибка', e)



@app.post('/register')
async def register_user(user: UserRegistration):
    try:
        return {"message": "User registered successfully", "user": user}
        return users
    except Exception as e:
        print('[INFO] Ошибка', e)
