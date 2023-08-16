import asyncio
import json
import random

import aiohttp
import pandas as pd


def process_single_response(symbol, response):
    result_dict = {}
    json_data = json.loads(
        response
    )  # Safely convert the string response to a dictionary

    # Check if the data is available
    if json_data["data"] and "shortInterestTable" in json_data["data"]:
        data = json_data["data"]["shortInterestTable"]["rows"]
        df = pd.DataFrame(data)
        result_dict[symbol] = df
    else:
        print(f"Data not available for {symbol}")

    return result_dict


def random_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    ]

    accept_languages = [
        "en-US,en;q=0.9",
        "en-GB,en;q=0.9",
        "en-CA,en;q=0.9",
        "en-AU,en;q=0.9",
    ]

    headers = {
        "authority": "api.nasdaq.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": random.choice(accept_languages),
        "dnt": "1",
        "origin": "https://www.nasdaq.com",
        "referer": "https://www.nasdaq.com/",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": random.choice(user_agents),
    }

    return headers


async def get_single_short_interest(symbol):
    url = f"https://api.nasdaq.com/api/quote/{symbol}/short-interest?assetClass=stocks"
    headers = random_headers()

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.text()


def get_data_from_nasdaq(symbol="AAPL"):
    response = asyncio.run(get_single_short_interest(symbol))
    result = process_single_response(symbol, response)

    # Display the dataframe
    for symbol, df in result.items():
        print(f"Results for {symbol}:")
        print(df)
        print("-" * 50)


get_data_from_nasdaq("AAPL")
