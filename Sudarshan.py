import requests
import telebot
from telebot import types
from app import keep_alive
import os

#weather api
def get_weather(getCity):
    city = getCity
    weather_key = os.environ.get('WEATHER_API')
    url = f"http://api.weatherapi.com/v1/current.json?key={weather_key}&q={city}"
    res = requests.get(url)
    
    if res.status_code == 200 :
        wdict = res.json()
        
        loc = wdict["location"]
        cur  = wdict["current"]
        return loc , cur
    else : 
        return "City not found"
        
def buttons(btnName) :
    btns = btnName
    markup = types.ReplyKeyboardMarkup(row_width = 4 , resize_keyboard = True)
    all_button = []
    for button in btns :   
        btn = types.KeyboardButton(button)
        all_button.append(btn)
    markup.add(*all_button)
    return markup


def tegbot() :
    indian_cities = [
    "New Delhi",
    "Azamgarh",
    "Orai",
    "Kanpur",
    "Lucknow",
    "Mumbai",
    "Jaipur",
    "Ahmedabad"
    ]
    botToken = os.environ.get('BOT_TOKEN')

    bot = telebot.TeleBot(botToken)

    #start massege response 
    @bot.message_handler(commands = ["start"])
    def send_message(message) :
        btn = buttons(['/weather'])
        bot.send_message(message.chat.id , "👋🏻Hyy, I am weather bot.",reply_markup = btn)
    
    #weather massage response 
    @bot.message_handler(commands = ["weather"])
    def send_message1(message) :
        btns = buttons(indian_cities)
        bot.send_message(message.chat.id, "✍🏻Enter your city name.", reply_markup = btns)
    
    #weather details responser
    @bot.message_handler(func = lambda message : True)
    def weather(message):
       try :
           loc , cur  = get_weather(message.text)
            #Here , I am showing all data .formate is dict.
           reply = (f"=====🌤️WEATHER REPORT☀️=====\n📍COUNTRY : {loc['country']}\n📍REGION  : {loc['region']}\n📍CITY     : {loc['name']}\n🗓️DATE & ⏳TIME : {loc['localtime']}\n🌡️TEMPERATURE : {cur['temp_c']}°C\n🔥FEELS TEMPRATURE : {cur['feelslike_c']}°C\n🥵HUMIDITY    : {cur['humidity']} %\n🍃WIND        : {cur['wind_kph']} km/h\n👁️VISIBILITY : {cur['vis_km']} km\n🔊Last Update : {cur['last_updated']}")
           bot.send_message(message.chat.id , reply)
       except ValueError :
           bot.send_message(message.chat.id , "City not found")
    keep_alive()
    print("Bot is running now .... ")
    bot.polling(none_stop = True)
    

if __name__ == "__main__" :
    try :
        tegbot()
    except Exception as e :
        print(f"eroor as {e}")