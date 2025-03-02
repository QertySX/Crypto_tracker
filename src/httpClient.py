import asyncio
import aiohttp
import json
from config import api_key


async def HTTPClient():
    try:
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': api_key,
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                result = await response.json()
                filterResponse = result['data']
                print(filterResponse)


    except Exception as e:
        print("[INFO] Ошибка ", e)

if __name__ == "__main__":
    asyncio.run(HTTPClient())