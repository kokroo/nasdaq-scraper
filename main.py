import asyncio

from data_processor import process_responses
from nasdaq_api import get_short_interest


def main():
    symbols = ["AAPL", "TSLA", "AMZN", "GOOG", "NVDA", "PLTR"]
    responses = asyncio.run(get_short_interest(symbols))

    results = process_responses(symbols, responses)

    # Display the dataframes
    for symbol, df in results.items():
        print(f"Results for {symbol}:")
        print(df)
        print("-" * 50)


if __name__ == "__main__":
    main()
