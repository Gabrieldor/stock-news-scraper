from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import time

"""elif "last month" in relative_time.lower():
        converted_time = now - relativedelta(months=1)
    elif "month" in relative_time and "ago" in relative_time:
        months_later = int(relative_time.split()[0])
        converted_time = now + relativedelta(months=months_later)"""

def convert_relative_time(relative_time):
    now = datetime.now()
    
    if "hour" in relative_time:
        hours_ago = int(relative_time.split()[0])
        converted_time = now - timedelta(hours=hours_ago)
    elif "yesterday" in relative_time.lower():
        converted_time = now - timedelta(days=1)
    elif "day" in relative_time:
        days_ago = int(relative_time.split()[0])
        converted_time = now - timedelta(days=days_ago)
    else:
        print(relative_time)
        raise ValueError("Unsupported relative time format")
    
    return converted_time.strftime("%b %d, %Y")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

#https://companiesmarketcap.com/tech/largest-tech-companies-by-market-cap/
symbols = ["TSM", "AVGO", "TCEHY", "ASML", "ORCL", "NFLX", "AMD", "QCOM"]

for symbol in symbols:
    time.sleep(30)
    data = []
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"https://finance.yahoo.com/quote/{symbol}/news/")
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='stream-item  svelte-7rcxn']")))

    company = driver.find_element(By.XPATH, "//h1[@class='svelte-3a2v0c']").text.split(" ")[0].lower()

    reached_page_end = False
    last_height = driver.execute_script("return document.body.scrollHeight")

    while not reached_page_end:
        driver.find_element(By.XPATH, "//body").send_keys(Keys.END)
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if last_height == new_height:
                reached_page_end = True
        else:
                last_height = new_height


    for div in driver.find_elements(By.XPATH, "//*[@class='stream-item  svelte-7rcxn']"):
        title = div.find_element(By.XPATH, "./section/div/a/h3").text
        if company not in title.lower() and symbol.lower() not in title.lower():
            continue
        try:
            date = convert_relative_time(div.find_element(By.XPATH, "./section/div/div/div[1]").text.split("\n")[-1])
        except:
            continue
        info = {"title": title, "date": date, "symbol": symbol}
        data.append(info)

    pd.DataFrame(data).to_csv("data.csv", index=False, mode="a", header=False)