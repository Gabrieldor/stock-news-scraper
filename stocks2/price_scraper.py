from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import pandas as pd
import time

def convert_to_datetime(date_str):
    # Parse the input date string
    date_obj = datetime.strptime(date_str, "%b %d, %Y")
    return date_obj


def scrap(symbol, target_date):

    if get == True:
        driver.get(f"https://finance.yahoo.com/quote/{symbol}/history/")
    wait.until(EC.presence_of_element_located((By.XPATH, "//tr[@class='svelte-ewueuo']")))
    rows = driver.find_elements(By.XPATH, "//tr[@class='svelte-ewueuo']")[1:]
    target_index = None
    for row in rows:
        target_datetime = convert_to_datetime(target_date)
        date = row.find_element(By.XPATH, "./td[1]").text
        if date == target_date:
            target_index = rows.index(row)
            break
        if target_datetime > convert_to_datetime(date):
            break

    if target_index == None: return None
    if target_index-6 < 0: return None
    try:
        prices = [float(rows[target_index-6].find_element(By.XPATH, "./td[2]").text.replace(",", "")),
                float(rows[target_index].find_element(By.XPATH, "./td[5]").text.replace(",", ""))]
    except:
        return None
    
    change = (prices[1]*100)/prices[0]
    print(prices[0], prices[1], change)

    if change > 110:
        result = 3
    elif change > 105:
        result = 2
    elif change >= 101:
        result = 1
    elif change < 90:
        result = -3
    elif change < 95:
        result = -2
    elif change <= 99:
        result = -1
    else:
        result = 0

    return result

    


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
df = pd.read_csv("data.csv")
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)
old_symbol = None
get = True

for index, row in df.iterrows():
    row_dict = row.to_dict()
    if row.iloc[2] != old_symbol:
        old_symbol = row.iloc[2]
        get = True
    else: get = False
    row_dict["result"] = scrap(row.iloc[2], row.iloc[1])
    pd.DataFrame([row_dict]).to_csv("prices.csv", header=False, index=False, mode="a")
    print(row_dict)

