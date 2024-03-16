[English](https://github.com/smallmin82465/Real-time-stock-and-options-data-collection-and-analysis-system/blob/main/README.md)

# 即時股票和期權數據收集與分析系統

這是一個基於Python的股票/期權分析系統，可以從Yahoo Finance獲取即時的股票和期權數據，並提供數據處理、查詢、驗證和可視化等功能。

## 功能特點

- 股票數據收集：根據用戶指定的股票代碼和時間間隔，從Yahoo Finance獲取即時股票數據，並將其保存為本地CSV文件。

- 期權數據收集：根據用戶指定的期權合約代碼和時間間隔，從Yahoo Finance獲取即時期權數據，並將其保存為本地CSV文件。

- 數據處理：對收集到的原始股票和期權數據進行預處理、合併、波動率計算和Black-Scholes理論定價等操作。

- 數據查詢：為用戶提供基於SQL的查詢接口，可以對處理後的結構化數據進行各種查詢和驗證。

- 數據可視化：內置豐富的數據可視化工具，用戶可以繪製不同股票或期權合約的歷史價格、波動率等指標的圖表。

## 安裝和使用

1. 從Github克隆此項目

2. 安裝必要的Python庫：
   ```
   pip install -r requirements.txt
   ```

3. 運行主程序：
   ```
   python mainUI.py
   ```

## 系統架構

本系統採用模塊化設計，主要包括以下核心模塊：

- 用戶界面（GUI）：基於PyQt5開發，為用戶提供簡潔直觀的操作界面。

- 股票數據收集模塊：調用yfinance庫，根據用戶指定的參數獲取歷史股票數據。

- 期權數據收集模塊：調用yfinance庫，根據用戶指定的參數獲取歷史期權數據。

- 數據處理模塊：使用pandas進行數據清洗、轉換和計算。

- 數據查詢模塊：使用sqlite3作為內置數據庫，為用戶提供SQL查詢功能。

- 數據可視化模塊：使用matplotlib進行數據繪圖和可視化呈現。
