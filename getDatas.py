import datetime
import json

import requests

from setting import load_env

global trends
trends = dict()


def getTrends():
    url = "https://datalab.naver.com/shoppingInsight/getKeywordRank.naver?timeUnit=date&cid=50000001"

    headers = {"Referer": "https://datalab.naver.com/", "User-Agent": "PostmanRuntime/7.35.0"}
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    response_body = response.json()

    for i in response_body:
        trends[i["date"]] = [x["keyword"] for x in i["ranks"]]


def getShoppingTrends(trend_keyword):
    url = "https://openapi.naver.com/v1/datalab/shopping/category/keywords"
    client_id, client_secret = load_env()
    print(client_id, client_secret)
    headers = dict()
    headers["X-Naver-Client-Id"] = client_id
    headers["X-Naver-Client-Secret"] = client_secret
    data = dict()
    data["startDate"] = str((datetime.datetime.today() - datetime.timedelta(weeks=4)).date())
    data["endDate"] = str(datetime.datetime.today().date())
    data["timeUnit"] = "date"
    data["category"] = "50000001"
    data["keyword"] = [{"name": f"{i}번째", "param": [trend_keyword[i]]} for i in range(len(trend_keyword))]
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_body = response.json()
    print(response_body)
    return response_body
