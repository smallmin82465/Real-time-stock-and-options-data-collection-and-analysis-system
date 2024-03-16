Real-time Stock and Options Data Collection and Analysis System
This is a Python-based stock/options analysis system that can retrieve real-time stock and options data from Yahoo Finance and provide functions such as data processing, querying, verification, and visualization.

Features
Stock Data Collection: Retrieve real-time stock data from Yahoo Finance based on user-specified stock symbols and time intervals, and save it as local CSV files.
Options Data Collection: Retrieve real-time options data from Yahoo Finance based on user-specified option contract symbols and time intervals, and save it as local CSV files.
Data Processing: Perform preprocessing, merging, volatility calculation, and Black-Scholes theoretical pricing on the collected raw stock and options data.
Data Querying: Provide an SQL-based query interface for users to perform various queries and verifications on the processed structured data.
Data Visualization: Built-in rich data visualization tools for users to plot charts of historical prices, volatility, and other indicators for different stocks or option contracts.
Installation and Usage
Clone this project from Github
Install the necessary Python libraries: pip install -r requirements.txt
Run the main program: python mainUI.py
System Architecture
This system adopts a modular design, mainly including the following core modules:

User Interface (GUI): Developed based on PyQt5, providing users with a concise and intuitive operation interface.
Stock Data Collection Module: Calls the yfinance library to retrieve historical stock data based on user-specified parameters.
Options Data Collection Module: Calls the yfinance library to retrieve historical options data based on user-specified parameters.
Data Processing Module: Uses pandas for data cleaning, conversion, and calculation.
Data Query Module: Uses sqlite3 as the built-in database to provide SQL query functions for users.
Data Visualization Module: Uses matplotlib for data plotting and visual presentation.
