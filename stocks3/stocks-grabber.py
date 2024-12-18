from iqoptionapi.stable_api import IQ_Option
import matplotlib.pyplot as plt
import time
import pandas as pd
from time import strftime, localtime
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
import itertools

iq = IQ_Option("YOUR_EMAIL","YOUR_PASSWORD")
iq.connect()
data = []
now = time.time()
size = 60

while len(data) < 50000:
    print(len(data))
    if len(data) == 0:
        now = time.time()
    info = iq.get_candles("NVDA:US", size, 1000 + 1, now)
    try:
        now = info[0]["from"] - size
    except:
        break
    for i in info[::-1]:
        data.append({"date": strftime('%Y-%m-%d %H:%M', localtime(i["from"])), "close": i["close"], "open": i["open"], "min": i["min"], "max": i["max"]})

df = pd.DataFrame(data)
df.to_csv("data.csv", index = False)
