import asyncio

import pandas as pd

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
    with pd.ExcelWriter("stock_data.xlsx") as writer:
        for symbol, df in results.items():
            # Convert settlementDate to datetime type
            df["settlementDate"] = pd.to_datetime(df["settlementDate"])

            # Convert interest and avgDailyShareVolume to float
            for col in ["interest", "avgDailyShareVolume"]:
                df[col] = df[col].str.replace(",", "").astype(float)

            df.to_excel(writer, sheet_name=symbol, index=False)


if __name__ == "__main__":
    main()
