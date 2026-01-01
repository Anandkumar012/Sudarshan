import telebot
from telebot import types
from app import keep_alive
import os
from weatherapi import get_weather
import random 
import threading
import json

#=============================================

#location file load in file ,this is for demo
def loc():
    try:
        path = "Chapter_location.json"
        with open(path , 'r' , encoding='utf-8') as file :
           data = json.load(file)
           return data
    except Exception as e:
        print("Chapter_location.json file not found",e)
        return None

#==============================================

#random option creation method
def random_opts(options) :
    opts = []
    while len(options) != 0 :
        ran_opt = random.choice(options)
        opts.append(ran_opt)
        options.remove(ran_opt)
    else :
        return opts

#==============================================
#json question load
def load_question(file_path, chapterNumber):
    try :
        with open(file_path , 'r' , encoding='utf-8') as file :
            load = json.load(file)
            return load[chapterNumber]
    except Exception as e :
        print(f"error as {e}")
        return None


#==============================================

#Keyboard button creation
def buttons(btnName) :
    markup = types.ReplyKeyboardMarkup(row_width = 4 , resize_keyboard = True)
    all_button = []
    for button in btnName :   
        btn = types.KeyboardButton(button)
        all_button.append(btnName)
    markup.add(*all_button)
    return markup

#==============================================

#INLINE BUTTONS CREMATION
def inline_buttons(btnName):
    markup = types.InlineKeyboardMarkup(row_width=1 if any(len(btn) >= 10 for btn in btnName ) else 3) 
    
    all_button = []    
    for button in btnName : 
        btn = types.InlineKeyboardButton(button,callback_data = button)
        all_button.append(btn)
    
    markup.add(*all_button)
    return markup

#=============================================

#quiz sent func
def sent_quiz_poll(bot , chat_id , chapNum,file_path) :
    #same id can not start 2 quiz in one time
    if chat_id in user_status:
        bot.send_message(chat_id , 'you are already start quiz.if you can stop your quiz send me /stop .')
        return
    try:
        load_que = load_question(file_path ,chapNum) #load quest according to chapter 
        que = random.choice(load_que)
        random.shuffle(que[1])  
        
        #bot send poll func
        send_poll = bot.send_poll(chat_id = chat_id,
            question = que[0],
            options = que[1],
            type = "quiz",
            correct_option_id = que[1].index(que[2]),
            is_anonymous = False,
            open_period = 15
                                  )
        
        #bot repeat questions func
        threading.Timer(15.3, sent_quiz_poll, args=[bot, chat_id ,chapNum , file_path]).start()
    except Exception as e :
        print(f"error as {e}")
        bot.send_message(chat_id, "⚠️ Sorry 😐 Internal issue, try later")
        return None

#==============================================

user_status = {}
bot_memory = {}

#==============================================

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

#==============================================

    #start massege response 
    @bot.message_handler(commands = ["start"])
    def send_message(message) :
        chat_id = message.chat.id
        user_status[chat_id] = 'BOT ACTIVE'
        res_button =buttons(['/weather','/quiz'])
        bot.send_message(chat_id , "👋🏻Hyy, I am  a bot.",reply_markup = res_button)

#==============================================
    
    #weather massage response 
    @bot.message_handler(commands = ["weather"])
    def send_message1(message) :
        btns = buttons(indian_cities)
        bot.send_message(message.chat.id, "✍🏻Enter your city name.", reply_markup = btns)
     
#==============================================
    
    #weather details responser
    @bot.message_handler(func = lambda message : not message.text.startswith('/'))
    def weather(message):
       try :
           loc, cur= get_weather(message.text)
            #Here , I am showing all data .formate is dict.
           reply = (f"=====🌤️WEATHER REPORT☀️=====\n📍COUNTRY : {loc['country']}\n📍REGION  : {loc['region']}\n📍CITY     : {loc['name']}\n🗓️DATE & ⏳TIME : {loc['localtime']}\n🌡️TEMPERATURE : {cur['temp_c']}°C\n🔥FEELS TEMPRATURE : {cur['feelslike_c']}°C\n🥵HUMIDITY    : {cur['humidity']} %\n🍃WIND        : {cur['wind_kph']} km/h\n👁️VISIBILITY : {cur['vis_km']} km\n🔊Last Update : {cur['last_updated']}")
           bot.send_message(message.chat.id , reply ,reply_markup = types.ReplyKeyboardRemove())
       except ValueError :
           bot.send_message(message.chat.id , "City not found")

#==============================================  
    
    @bot.message_handler(commands = ["quiz"])
    def quiz(message) :
        chat_id = message.chat.id
        class_button = ['CLASS 12','CLASS 09']
        all_btn = inline_buttons(class_button)
        bot.send_message(chat_id, '✍🏻 SELECET YOUR CLASS.',reply_markup = all_btn)
        bot.send_message(chat_id, 'SORRY , This bot is working condition becasuse at present data are not available for bot\nIt is working only for class 12 → physics\nI will all data for this bot early',reply_markup = types.ReplyKeyboardRemove())
        user_status[chat_id] = 'QUIZ MOD ACTIVATE'

#==============================================
           
    #CLASS handler    
    @bot.callback_query_handler(func = lambda call : call.data.startswith('CLASS'))
    def class_handler(call) :
        className = call.data.replace(" ","_")
        chat_id = call.message.chat.id
        bot.answer_callback_query(call.id)
        location = loc()
        if location is None or className not in location:
            print("class not found")
            bot.send_message(chat_id, '🤖 Class not in data.')
            return
        sub_list = list(location[className].keys())
        all_btn = inline_buttons(sub_list)
        bot.send_message(chat_id, '✍🏻 SELECT YOUR SUBJECT.',reply_markup = all_btn)
        bot_memory[chat_id] = className    
    
#==============================================
 
    #SUBJECT handler 
    @bot.callback_query_handler(func = lambda call : call.data.startswith('SUB ~ '))
    def subject_handler(call) :
        chat_id = call.message.chat.id
        bot.answer_callback_query(call.id)
        location = loc()
        if location is None :
            print("Subject not found")
            bot.send_message(chat_id, '🤖 Subject not in data.')
            return
        all_chap = list(location[bot_memory.get(chat_id)][call.data]
        ) #facth chapter's in location file
        all_btn = inline_buttons(all_chap)
        bot.send_message(chat_id , '✍🏻 SELECT YOUR CHAPTER.', reply_markup = all_btn)
        bot_memory[f"SUB{chat_id}"] = call.data.removeprefix('SUB ~ ')
        
 #==============================================
       
    #CHAPTER handler  
    @bot.callback_query_handler(func = lambda call : call.data.startswith('Ch~'))
    def question(call) :
        chat_id = call.message.chat.id
        chapNum = call.data[:5]
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, '📢 Quiz START')
        user_status[chat_id] = 'QUIZ START'
        #this condition remove in feature.
        if bot_memory.get(f'SUB{chat_id}') == 'PHYSICS' :
            file_path = f"{bot_memory[chat_id]}_{bot_memory[f'SUB{chat_id}']}_DATASET.json"
            sent_quiz_poll(bot , chat_id , chapNum,file_path)
        else :
            bot.send_message(chat_id, '🥲SORRY, At this time bot has only PHYSICS data .')

#==============================================

    @bot.message_handler(commands = ["stop"])
    def stop_bot(message) :
        chat_id = message.chat.id
        if user_status.get(chat_id) == 'QUIZ START' :
            user_name = message.from_user.first_name
            stop_text = (
                f"📌NOTICE📌\n\n"
                f"👤 QUIZ STOPPED by {user_name}.\n"
                f"✍🏻 If you want to restart quiz sent me /quiz")
            del user_status[chat_id]
            if chat_id in bot_memory :
                del bot_memory[chat_id]
            if f"SUB{chat_id}" in bot_memory :
                del bot_memory[f"SUB{chat_id}"]
            bot.send_message(chat_id , stop_text)
        else :
            bot.send_message(chat_id ,"🤖 There is no active process running right now.You can /start one anytime.")
            
#=============================================

    keep_alive()
    print("Bot is running now .... ")
    try :
        bot.infinity_polling(timeout=60, long_polling_timeout=60,allowed_updates=["message", "poll", "poll_answer","callback_query"])
    except Exception as e:
        print("polling error :", e)
    
#==============================================

if __name__ == "__main__" :
    try :
        tegbot()
    except Exception as e :
        print(f"error as {e}")