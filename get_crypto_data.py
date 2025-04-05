import logging
from config import api_key
import aiohttp

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
                    logging.error(f'[INFO] Ошибка {response.status}')
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