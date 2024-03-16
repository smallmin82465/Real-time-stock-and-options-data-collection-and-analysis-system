import pandas as pd
import yfinance as yf
from datetime import date, timedelta
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def optionget_min(symbols,DataInterval="1m", DataPeriod="1d"):
    """
    optionget_min(symbols)
    symbols: stock code, which can be list()
    Capture the option of the stock symbol of symbols + stock information
    Each contractSymbol can capture data with an interval of one minute from 1 to 7 days ago
    Save as a CSV file Today_Symbols.csv
    """
    for sym in symbols:
        tk = yf.Ticker(sym)
        exp = tk.options
        options = pd.DataFrame()  # 空的dataframe保存結果
        result = pd.DataFrame()   # 空的dataframe保存結果
        
        for i in exp:
            opt = tk.option_chain(i).calls
            options = options.append(opt, ignore_index=True) 
        contract = options[options['volume'] >= 10]['contractSymbol']    # 篩選數量>=10的選擇權
        for e in contract:
            ticker = yf.Ticker(e)
            option_data = ticker.history(DataPeriod, interval=DataInterval)
            option_data['contractSymbol'] = e  # 添加contractSymbol列
            option_data.insert(0, 'Datetime', option_data.index)  # 將Datetime列插入到第一列位置
            # 將Open, High, Low, Close列保留到小數後兩位四捨五入
            option_data[['Open', 'High', 'Low', 'Close']] = option_data[['Open', 'High', 'Low', 'Close']].round(2)  
            # 選擇需要的欄位
            option_data = option_data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume', 'contractSymbol']]  
            result = result.append(option_data, ignore_index=True)  # 將結果保存到result
        # 切割出股票代號
        result['Ticker'] = result['contractSymbol'].str.extract('([A-Za-z]{2,4})')  
        # 切割出到期日
        result['Expiration_Date'] = pd.to_datetime(result['contractSymbol'].str.extract('([A-Za-z]+(\d+))')[1], format='%y%m%d') 
        # 切割出CALL_PUT 
        result['CALL_PUT'] = result['contractSymbol'].str.extract('([A-Za-z]{2,4})(\d+)([CP])')[2].map({'C': 'CALL', 'P': 'PUT'})  
        result['Strike'] = result['contractSymbol'].str.extract('(\d+)$').astype(float) / 1000  # 切割出履約價
        result['Datetime'] = pd.to_datetime(result['Datetime'])
        
        stock_ticker = yf.Ticker(sym)
        stock_price = stock_ticker.history(DataPeriod, interval=DataInterval)
        stock_price = stock_price[['Close']].round(2)
        stock_price.columns = ['stockPrice']
        stock_price.reset_index(inplace=True)
        stock_price = stock_price[['Datetime', 'stockPrice']]
        stock_price.reset_index(drop=True, inplace=True)
        
        df_merged = pd.merge(result, stock_price, on='Datetime', how='left')
        today = date.today().strftime("%Y-%m-%d")
        csv_filename = today + "_" + sym + ".csv"  # 命名格式 Date_Ticker.csv
        df_merged.to_csv(csv_filename, index=False)  # 保存到csv

ticker_list = ["SPY","QQQ","VT","DIA","BND","IWN","XLF","SOXX","AAPL","NVDA","MSFT","GOOG"]
ticker_list1 = ['XLE', 'XLU', 'XLK', 'XLB', 'XLP', 'XLY', 'XLI', 'XLV', 'XLF', 'XLRE', 'XLC']
optionget_min(ticker_list)
optionget_min(ticker_list1)