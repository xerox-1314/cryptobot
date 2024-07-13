import time
import json
import schedule
from main import send_up, send_down
from pybit.unified_trading import HTTP
session = HTTP(testnet=False)


def get_not_price():
    price = session.get_tickers(
        category="inverse",
        symbol="NOTUSDT")['result']['list'][0]['indexPrice']
    return float(price)


def check_change_price():
    with open('info.json', 'r') as file:
        info = json.load(file)
    price_now = get_not_price()
    change = (price_now/info['last_price'] - 1)*100
    if abs(change) >= info['procent']:
        if change > 0:
            send_up(change, price_now)
        else:
            send_down(abs(change), price_now)


def work():
    schedule.every().second.do(check_change_price)
    while True:
        schedule.run_pending()
        time.sleep(1)
