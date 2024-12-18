import requests
from bs4 import BeautifulSoup
import pandas as pd


html = requests.get("https://www.nbcnews.com/tech/apple").content

bs = BeautifulSoup(html, features="lxml")
news = []
data = []

for h2 in bs.find_all("h2"):
    try:
        a = h2.find_all("a", href=True)[0]
        if a.find_all("span", {"class": "tease-card__headline"}):
            news.append(a["href"])
    except:
        pass


for new in news:
    html = requests.get(new).content
    bs = BeautifulSoup(html, features="lxml")
    title = bs.find_all("h1")[0].text
    time = ",".join(bs.find_all("time")[0].text.split(",")[:2])
    info = {"title": title, "time": time}
    data.append(info)

pd.DataFrame(data).to_csv("data_appl.csv")