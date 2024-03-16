import yfinance as yf
from datetime import date
def get_stock_price(symbols, folder_path=None, DataInterval="1m", DataPeriod="2d", progress_callback=None):
    # Define the stock symbol and date range
    for sym in symbols:
        stock = yf.Ticker(sym)
        # Get the stock price data
        stock_price = stock.history(period=DataPeriod, interval=DataInterval)
        stock_price.reset_index(inplace=True)
        stock_price['Ticker'] = sym
        today = date.today().strftime("%Y-%m-%d")
        csv_filename = today + "_" + sym + "_stock" + ".csv"  # Date_Ticker_stock.csv
        stock_price.to_csv(folder_path + '/' + csv_filename, index=False)

        # If a progress callback is provided, call it with the current progress
        if progress_callback:
            progress_callback(100)  # Assuming the progress is complete (100%)
