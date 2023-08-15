import json

import pandas as pd


def process_responses(stock_symbols, responses):
    result_dict = {}

    for symbol, response in zip(stock_symbols, responses):
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
