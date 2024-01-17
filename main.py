import requests
import os
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


stock_params ={
    "function": "TIME_SERIES_DAILY",
    "symbol": f"{STOCK}",
    "apikey": os.environ.get("STOCK_API_KEY")
}

news_params = {
    "apikey": os.environ.get("NEWS_API_KEY"),
    "q": f"{COMPANY_NAME}",
    "searchIn": "Title",
    "from": "2024-01-01",
    "to": "2024-01-17",
    "pageSize": 3,
    "language": "en"
}


response = requests.get(url="https://www.alphavantage.co/query?", params=stock_params)
data = response.json()["Time Series (Daily)"]
time_series = [value for (key, value) in data.items()]
yesterday_price = float(time_series[0]["4. close"])
b_yesterday = float(time_series[1]["4. close"])
diff = abs(yesterday_price - b_yesterday)
diff_percentage = (diff / yesterday_price) * 100
if diff_percentage > 5:
    news_response = requests.get(url="https://newsapi.org/v2/everything?", params=news_params)
    news_data = news_response.json()
    news_series = [value for (key,value) in news_data.items()][2]
    formatted_news = [f"Healine: {article["title"]}. \nBrief: {article["description"]}" for article in news_series]
    # for news in formatted_news:






