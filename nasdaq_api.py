import asyncio

import aiohttp

from anti_block import random_headers


async def get_short_interest(stock_symbols=["AAPL"]):
    async def fetch_single_symbol(symbol):
        url = f"https://api.nasdaq.com/api/quote/{symbol}/short-interest?assetClass=stocks"
        headers = random_headers()

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.text()

    results = await asyncio.gather(
        *(fetch_single_symbol(symbol) for symbol in stock_symbols)
    )
    return results
