import yfinance as yf
import pandas as pd

ticker = yf.Ticker("^IXIC")
data = ticker.history(period = "max",interval="1d")
# print(data.tail())
# print(data.rpow)
# print(len(data)) # gives us the number of rows
# print(data["Open"].iloc[0])
# print(data.index[-1])
print(data.head())


print(data.columns)
