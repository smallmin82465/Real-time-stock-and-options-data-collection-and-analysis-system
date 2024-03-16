import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm

def calculate_volatility(file_path, progress_callback=None):
    df = pd.read_csv(file_path)
    required_columns = ['Ticker', 'Datetime']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Error: Missing required columns: {', '.join(missing_columns)}")
    tickers = list(set(df['Ticker']))
    start_date = (datetime.strptime(df['Datetime'].min(), '%Y-%m-%d %H:%M:%S%z') - timedelta(days=365)).strftime('%Y-%m-%d')
    end_date = df['Datetime'].max().split(" ")[0]

    data = yf.download(tickers, start=start_date, end=end_date)

    # Initialize tqdm for progress tracking
    tqdm_iterator = tqdm(df.iterrows(), total=len(df), desc='Calculating Volatility', leave=False, position=0)

    for index, row in tqdm_iterator:
        ticker = row['Ticker']
        start_date = datetime.strptime(row['Datetime'], '%Y-%m-%d %H:%M:%S%z') - timedelta(days=365)
        start_date_np = np.datetime64(start_date)
        end_date = datetime.strptime(row['Datetime'], '%Y-%m-%d %H:%M:%S%z') - timedelta(days=1)
        end_date_np = np.datetime64(end_date)

        if len(tickers) == 1:
            stock_data = data['Adj Close'][(data.index >= start_date_np) & (data.index <= end_date_np)]
        else:
            stock_data = data['Adj Close'][ticker][(data.index >= start_date_np) & (data.index <= end_date_np)]

        volatility = stock_data.pct_change().std() * (252**0.5)
        df.at[index, 'Volatility'] = volatility

        # Call progress_callback to update the progress bar
        if progress_callback:
            progress_callback(int((index + 1) / len(df) * 100))

    tqdm_iterator.close()

    output_file_path = file_path.replace('.csv', '_output.csv')
    df.to_csv(output_file_path, index=False)
