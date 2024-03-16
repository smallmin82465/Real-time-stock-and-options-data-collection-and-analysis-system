import pandas as pd
import yfinance as yf
from datetime import date
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def optionget_min(symbols, folder_path=None, progress_dialog=None, DataInterval="1m", DataPeriod="2d"):
   """
   optionget_min(symbols)
   symbols: stock symbols, can be list()
   Download option and stock data for the given symbols
   Each contractSymbol can fetch data from 1 to 7 days ago with a time interval of one minute
   Save as csv file Today_Symbols.csv
   """
   for sym in symbols:
       tk = yf.Ticker(sym)
       exp = tk.options
       options = pd.DataFrame()  # Empty dataframe to store results
       result = pd.DataFrame()   # Empty dataframe to store results
       
       for i in exp:
           opt = tk.option_chain(i).calls
           options = options.append(opt, ignore_index=True)  # Append call and put for each expiration date
       contract = options[options['volume'] >= 10]['contractSymbol']    # Filter options with volume >= 10
       for e in contract:
           if progress_dialog and progress_dialog.wasCanceled():
               return  # Check if cancel button pressed
           ticker = yf.Ticker(e)
           option_data = ticker.history(period=DataPeriod, interval=DataInterval)
           option_data['contractSymbol'] = e  # Add contractSymbol column
           option_data.insert(0, 'Datetime', option_data.index)  # Insert Datetime column at the first position
           # Round Open, High, Low, Close columns to two decimal places
           option_data[['Open', 'High', 'Low', 'Close']] = option_data[['Open', 'High', 'Low', 'Close']].round(2)  
           # Select required columns
           option_data = option_data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume', 'contractSymbol']]  
           result = result.append(option_data, ignore_index=True)  # Store results in result
       # Extract ticker symbol
       result['Ticker'] = result['contractSymbol'].str.extract('([A-Za-z]{2,4})')  
       # Extract expiration date
       result['Expiration_Date'] = pd.to_datetime(result['contractSymbol'].str.extract('([A-Za-z]+(\d+))')[1], format='%y%m%d') 
       # Extract CALL/PUT
       result['CALL_PUT'] = result['contractSymbol'].str.extract('([A-Za-z]{2,4})(\d+)([CP])')[2].map({'C': 'CALL', 'P': 'PUT'})  
       result['Strike'] = result['contractSymbol'].str.extract('(\d+)$').astype(float) / 1000  # Extract strike price
       result['Datetime'] = pd.to_datetime(result['Datetime'])
       
       stock_ticker = yf.Ticker(sym)
       stock_price = stock_ticker.history(period=DataPeriod, interval=DataInterval)
       stock_price = stock_price[['Close']].round(2)
       stock_price.columns = ['stockPrice']
       stock_price.reset_index(inplace=True)
       stock_price = stock_price[['Datetime', 'stockPrice']]
       stock_price.reset_index(drop=True, inplace=True)
       
       df_merged = pd.merge(result, stock_price, on='Datetime', how='left')
       today = date.today().strftime("%Y-%m-%d")
       csv_filename = today + "_" + sym + "_option" + ".csv"  # Naming format Date_Ticker.csv
       df_merged.to_csv(folder_path + '/' + csv_filename, index=False)