import aiohttp
from config import api_key
from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
import logging
from typing import List
from pydantic import BaseModel
import asyncio


app = FastAPI()

templates = Jinja2Templates(directory="templates")


logging.basicConfig(level=logging.DEBUG)

    # ФУНКЦИЯ ДЛЯ ЗАПРОСА API И ПОЛУЧЕНИЮ СПИСКА КРИПТОВАЛЮТ
async def get_raw_crypto_data():
    try:
        logging.debug("Получение данных криптовалюты...")
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': api_key,
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:

                if response.status == 200:
                    result = await response.json()
                    logging.debug("[INFO] Данные получены!")
                    return result
                else:
                    logging.error(f'[INFO] Ошибка: {response.status}' )
                    return {f"[INFO] HTTP ошибка: {response.status}"}

    except Exception as e:
        print('[INFO] Ошибка: ', e)

async def process_crypto_data() -> dict:
    raw_crypto_data = await get_raw_crypto_data()

    all_data = dict()

    for crypto in raw_crypto_data['data']:
        necessary_data = {
            "price": crypto['quote']['USD']['price'],
            "volume_24h": crypto['quote']['USD']['volume_24h'],
            "percent_change_24h": crypto['quote']['USD']['percent_change_24h'],
            "market_cap": crypto['quote']['USD']['market_cap']
        }
        all_data[crypto['name']] = necessary_data

    logging.info("[INFO] Данные обработаны!")
    return all_data



