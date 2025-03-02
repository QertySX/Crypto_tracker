import asyncio
import aiohttp
import json
from config import api_key
import fastapi

app = FASTAPI()

async def HTTPClient():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }