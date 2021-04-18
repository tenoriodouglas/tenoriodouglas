#!/usr/bin/python3.6
import telepot, urllib3
from telepot.loop import MessageLoop
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json, urllib.request
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from unidecode import unidecode

bot = telepot.Bot('908840680:AAFIPWgGnOvkLaOmNNdwkYeLnTyMKQ8eizs')

def processabi(pair):
    json_url = urllib.request.urlopen('https://api.kraken.com/0/public/Trades?pair='+pair)
    data = json.loads(json_url.read())
    if "result" in data:
        df = pd.DataFrame(data["result"])
        _pair = df.keys()

        price=[]
        date=[]
        for item in df[_pair[0]]:
            price.append(float(item[0]))
            date.append(int(item[2]))

        df["price"] = price
        df["date"] = pd.to_datetime(date, unit="s")
        #df["date"] = df["date"].dt.time

        sns.set_theme(style="darkgrid")
        df.plot(kind='line',x='date',y='price',legend=False)
        plt.title(_pair[0],size=16)
        plt.ylabel('Price')
        plt.xlabel('Date')
        plt.savefig('image.png',bbox_inches="tight")
        return True

def handle(msg):
    telepot.glance(msg)
    pair=unidecode(msg['text'].replace(" ",""))
    processabi(pair)
    if processabi(pair)==True:
        bot.sendPhoto(msg['from']['id'],photo=open('image.png', 'rb'))
    else:
        bot.sendMessage(msg['from']['id'], 'Par de ativos desconhecido!')

MessageLoop(bot, handle).run_as_thread()
