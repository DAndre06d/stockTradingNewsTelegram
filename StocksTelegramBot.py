import os
import requests
from datetime import datetime, timedelta

date = datetime.now()
formatted_date_now = date.strftime("%Y-%m-%d")
two_weeks_ago_date = date - timedelta(weeks=2)
formatted_two_weeks_ago_date = two_weeks_ago_date.strftime("%Y-%m-%d")
class StocksTelegramBot:
    def __init__(self, stock_symbol, company_name):
        self.stock = stock_symbol
        self.current_date = formatted_date_now
        self.two_weeks_ago = formatted_two_weeks_ago_date
        self.company_name = company_name
        self.stock_api_key = os.environ.get("STOCK_API_KEY")
        self.news_api_key = os.environ.get("NEWS_API_KEY")
        self.telegram_bot_token = os.environ.get("TELEGRAM_BOT")
        self.telegram_bot_chatid = os.environ.get("TELEGRAM_BOT_ID")
        self.get_stock_data()

    def telegram_bot_sendtext(self, bot_message: str):
        """Sends a message to alert the user about the stock price and news about it"""
        bot_token = os.environ.get("TELEGRAM_BOT")
        bot_chatid = os.environ.get("TELEGRAM_BOT_ID")
        send_text = ('https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatid +
                     '&parse_mode=Markdown&text=' + bot_message)
        response_bot = requests.get(send_text)
        return response_bot.json()

    def get_stock_data(self):
        stock_params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": f"{self.stock}",
            "apikey": self.stock_api_key
        }
        news_params = {
            "q": f"{self.company_name}",
            "searchIn": "Title",
            "from": f"{self.two_weeks_ago}",
            "to": f'{self.current_date}',
            "pageSize": 3,
            "language": "en"
        }
        news_headers = {
            "X-Api-Key": self.news_api_key
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
        print(diff_percentage)

        # checks if the percentage is greater than 5% if it is greater than 5% it will send a message
        if abs(diff_percentage) > 3:
            news_response = requests.get(url="https://newsapi.org/v2/everything?", params=news_params, headers=news_headers)
            news_data = news_response.json()
            news_series = [value for (key, value) in news_data.items()][2]
            print(news_series)
            formatted_news = [(f"{self.stock} {emoji}{diff_percentage}%\nHeadline: {article["title"]}. \nBrief: "
                               f"{article["description"]}") for article in news_series]
            for news in formatted_news:
                bot_messages = self.telegram_bot_sendtext(news)
