import telebot
import json
import schedule
import time
from config import token
from pybit.unified_trading import HTTP
bot = telebot.TeleBot(token)


class API:
    def __init__(self):
        self.session = HTTP(testnet=False)
        self.last_price = 0
        self.procent = 0

    def get_not_price(self):
        price = self.session.get_tickers(
            category="inverse",
            symbol="NOTUSDT")['result']['list'][0]['indexPrice']
        return float(price)

    def check_change_price(self, chat_id):
        with open('info.json', 'r') as file:
            info = json.load(file)
        price_now = self.get_not_price()
        change = (price_now / info['last_price'] - 1) * 100
        if abs(change) >= info['procent']:
            with open('info.json', 'w') as file:
                json.dump({'procent': info['procent'], "last_price": price_now}, file)
            if change > 0:
                send_up(change, price_now, chat_id)
            else:
                send_down(abs(change), price_now, chat_id)


api = API()


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Приветствую, дорогой друг. Я - бот, который может помочь следить за движением цены NOTCOIN, '
                     'что позволит сделать торговлю им безопаснее\n🔸 /help - вызвать список команд\n'
                                      '🔸 /check - отслеживать движение курса NOT\n🔸 /price - узнать текущую цену NOT'
                                      '\n🔸 /trade - совершить сделку (на разработке)')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Вот список моих команд:\n🔸 /help - вызвать список команд\n'
                                      '🔸 /check - отслеживать движение курса NOT\n🔸 /price - узнать текущую цену NOT'
                                      '\n🔸 /trade - совершить сделку (на разработке)')


@bot.message_handler(commands=['price'])
def price(message):
    bot.send_message(message.chat.id, f'✈️ Текущий курс NOT: {api.get_not_price()} USDT')


@bot.message_handler(commands=['check'])
def check(message):
    k = bot.send_message(message.chat.id, '📈 Монета для отслеживания: NOT\nНапиши процент изменения цены, '
                                          'который ты хочешь отслеживать.\nНо запомни:')
    bot.register_next_step_handler(k, check2)
    stick = open('stickers/norisk.webp', 'rb')
    bot.send_sticker(message.chat.id, stick)


def check2(message):
    if message.text is None:
        k = bot.send_message(message.chat.id, '😡 Ты че тупой что ли? Напиши ЧИСЛО > 0')
        bot.register_next_step_handler(k, check2)
    else:
        if message.text.replace(".", "", 1).isdigit() and float(message.text) > 0:
            procent = float(message.text)
            last_price = api.get_not_price()
            with open('info.json', 'w') as file:
                json.dump({'procent': procent, "last_price": last_price}, file)
            bot.send_message(message.chat.id,
                             f'Супер! Теперь я буду оповещать тебя сразу, как только цена NOT изменится на {procent} %')
            work(message.chat.id)

        else:
            k = bot.send_message(message.chat.id, '😡 Ты че тупой что ли? Напиши ЧИСЛО > 0')
            bot.register_next_step_handler(k, check2)


def send_up(change, price_now, chat_id):
    bot.send_message(chat_id, f'🟢 Цена NOT изменилась на +{change} %. Текущий курс: {price_now}')


def send_down(change, price_now, chat_id):
    bot.send_message(chat_id, f'🔴 Цена NOT изменилась на -{change} %. Текущий курс: {price_now}')


def work(chat_id):
    schedule.every().second.do(api.check_change_price, chat_id)
    while True:
        schedule.run_pending()
        time.sleep(1)


bot.polling(none_stop=True)