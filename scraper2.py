import requests
import pandas as pd
from datetime import datetime


def convert_date(date_str):
    # Parse the input date string
    parsed_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    # Format the parsed date into the desired output format
    formatted_date = parsed_date.strftime("%b %d, %Y")
    
    return formatted_date

url = "https://www.reuters.com/pf/api/v3/content/fetch/articles-by-section-alias-or-id-v1"
data = []

for i in range(0, 1000000, 20):

    querystring = {"query":"{\"arc-site\":\"reuters\",\"fetch_type\":\"collection\",\"id\":\"/technology/\",\"offset\":" + str(i) +",\"section_id\":\"/technology/\",\"size\":20,\"uri\":\"/technology/\",\"website\":\"reuters\"}","d":"194","_website":"reuters"}
    response = requests.request("GET", url, params=querystring)

    try:
        for article in response.json()["result"]["articles"]:
            title = article["basic_headline"]
            date = convert_date(article["published_time"])
            info = {"title": title, "date": date}
            data.append(info)
    except:
        break

    print(f"On {i}")
    


pd.DataFrame(data).to_csv("data.csv", index=False)
