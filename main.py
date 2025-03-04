import aiohttp
from config import api_key
from fastapi import FastAPI, Query


app = FastAPI()

@app.get("/crypto")
async def get_crypto():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            result = await response.json()
            all_data = {}
            for crypto in result['data']:  
                name = crypto['name']
                crypto_data = crypto['quote']['USD']
                necessary_data = {
                    crypto_data['price'],
                    crypto_data['volume_24h'],
                    crypto_data['percent_change_24h'],
                    crypto_data['market_cap']
                }
                all_data[name] = necessary_data  

            return all_data


@app.get("/crypto/portfolio")
async def get_portfolio():
    pass