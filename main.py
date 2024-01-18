import requests
import os
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


def telegram_bot_sendtext(bot_message):
    """Sends a message to alert the user about the stock price and news about it"""
    bot_token = os.environ.get("TELEGRAM_BOT")
    bot_chatid = os.environ.get("TELEGRAM_BOT_ID")
    send_text = ('https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatid +
                 '&parse_mode=Markdown&text=' + bot_message)
    response_bot = requests.get(send_text)
    return response_bot.json()


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
diff = yesterday_price - b_yesterday
emoji = None
if diff > 0:
    emoji = "🔺"
else:
    emoji = "🔻"

# Calculate the percentage
diff_percentage = round((diff / yesterday_price) * 100)

# checks if the percentage is greater than 5% if it is greater than 5% it will send a message
if abs(diff_percentage) > 5:
    news_response = requests.get(url="https://newsapi.org/v2/everything?", params=news_params)
    news_data = news_response.json()
    news_series = [value for (key,value) in news_data.items()][2]
    formatted_news = [(f"{STOCK} {emoji}{diff_percentage}%\nHeadline: {article["title"]}. \nBrief: "
                       f"{article["description"]}") for article in news_series]
    print(formatted_news)
    for news in formatted_news:
        bot_messages = telegram_bot_sendtext(news)






