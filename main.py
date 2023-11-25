import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
import os

def asdf():
    # load .env
    load_dotenv()
    client_id = os.environ.get('CLIENTID')
    client_secret = os.environ.get('CLIENTSECRET')
    url = "https://datalab.naver.com/shoppingInsight/getKeywordRank.naver?timeUnit=date&cid=50000001"
    trends = {}

    headers = {"Referer": "https://datalab.naver.com/", "User-Agent": "PostmanRuntime/7.35.0"}
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    response_body = response.json()

    for i in response_body:
         trends[i["date"]] = [x["keyword"] for x in i["ranks"]]

    df = pd.DataFrame.from_dict(trends)
    df = df.transpose()

    # Step 1: Reconstruct the DataFrame to track rank changes for each keyword
    ranked_df = pd.DataFrame()

    for col in df.columns:
        for idx, keyword in df[col].items():
            if keyword not in ranked_df.columns:
                ranked_df[keyword] = np.nan
            ranked_df.at[idx, keyword] = col + 1


    # Step 2: Plot the rank changes for each keyword
    plt.figure(figsize=(20,10))

    for column in ranked_df.columns:
        plt.plot(ranked_df.index, ranked_df[column], marker='', linewidth=1, alpha=0.9, label=column)
    plt.rc('font', family='Malgun Gothic')
    plt.legend(loc=2, ncol=2)
    plt.title("Keyword Rank Changes Over Time", loc='left', fontsize=12, fontweight=0, color='orange')
    plt.xlabel("Date")
    plt.ylabel("Rank")
    plt.gca().invert_yaxis()
    plt.yticks(range(11))
    # plt.show()
    return plt
    print(ranked_df)
