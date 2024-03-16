import numpy as np
import pandas as pd
from scipy.stats import norm
from tqdm import tqdm 

def calculate_blackscholes(file_path, progress_callback=None):
    df = pd.read_csv(file_path)
    # Check if all required columns exist
    required_columns = ['stockPrice', 'Strike', 'Volatility', 'Datetime', 'Expiration_Date']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Error: Missing required columns: {', '.join(missing_columns)}")

    # Data preprocessing
    df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce', utc=True)
    df['Datetime'] = pd.to_datetime(df['Datetime']).dt.tz_localize(None)
    df['Expiration_Date'] = pd.to_datetime(df['Expiration_Date'])
    df['Time_to_Expiration'] = (
        df['Expiration_Date'] - df['Datetime']) / pd.Timedelta(days=365)

    df['Time_to_Expiration_Day'] = (df['Expiration_Date'] - df['Datetime']).dt.days
    tqdm_iterator = tqdm(df.iterrows(), total=len(df), desc='Calculating Black-Scholes', leave=False, position=0)

    for index, row in tqdm_iterator:
        S = row['stockPrice']
        K = row['Strike']
        τ = row['Time_to_Expiration']
        r = 0.02319  # 10-year US Treasury bond yield as the unified risk-free rate for all stocks
        σ = row['Volatility']  

        d1 = (np.log(S / K) + (r + 0.5 * σ**2) * τ) / (σ * np.sqrt(τ))
        d2 = d1 - σ * np.sqrt(τ)

        # norm.cdf Normal Distribution Cumulative Distribution Function，CDF
        option_value = S * norm.cdf(d1) - K * np.exp(-r * τ) * norm.cdf(d2)

        df.at[index, 'Black_Scholes_Value'] = option_value

        # Call progress_callback to update the progress bar
        if progress_callback:
            progress_callback(int((index + 1) / len(df) * 100))

    tqdm_iterator.close()
    df.to_csv(file_path.replace('.csv', '.csv'), index=False)
