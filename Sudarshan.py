import telebot
from telebot import types
from app import keep_alive
import os
from weatherapi import get_weather
import random 
import threading

#location file load in file ,this is for demo
location = {
    'CLASS 12': {
        'SUB ~ PHYSICS': [
            'Ch~01 ELECTRIC CHARGES & FIELDS',
            'Ch~02 ELECTROSTATIC POTENTIAL & CAPACITANCE',
            'Ch~03 CURRENT ELECTRICITY',
            'Ch~04 MOVING CHARGES & MAGNETISM',
            'Ch~05 MAGNETISM & MATTER',
            'Ch~06 ELECTROMAGNETIC INDUCTION',
            'Ch~07 ALTERNATING CURRENT',
            'Ch~08 ELECTROMAGNETIC WAVES',
            'Ch~09 RAY OPTICS & OPTICAL INSTRUMENTS',
            'Ch~10 WAVE OPTICS',
            'Ch~11 DUAL NATURE OF RADIATION & MATTER',
            'Ch~12 ATOMS',
            'Ch~13 NUCLEI',
            'Ch~14 SEMICONDUCTOR ELECTRONICS'
        ],

        'SUB ~ CHEMISTRY': [
            'Ch~01 SOLID STATE',
            'Ch~02 SOLUTIONS',
            'Ch~03 ELECTROCHEMISTRY',
            'Ch~04 CHEMICAL KINETICS',
            'Ch~05 SURFACE CHEMISTRY',
            'Ch~06 GENERAL PRINCIPLES & PROCESSES OF ISOLATION OF ELEMENTS',
            'Ch~07 p-BLOCK ELEMENTS',
            'Ch~08 d & f BLOCK ELEMENTS',
            'Ch~09 COORDINATION COMPOUNDS',
            'Ch~10 HALOALKANES & HALOARENES',
            'Ch~11 ALCOHOLS, PHENOLS & ETHERS',
            'Ch~12 ALDEHYDES, KETONES & CARBOXYLIC ACIDS',
            'Ch~13 AMINES',
            'Ch~14 BIOMOLECULES',
            'Ch~15 POLYMERS',
            'Ch~16 CHEMISTRY IN EVERYDAY LIFE'
        ],

        'SUB ~ MATHEMATICS': [
            'Ch~01 RELATIONS & FUNCTIONS',
            'Ch~02 INVERSE TRIGONOMETRIC FUNCTIONS',
            'Ch~03 MATRICES',
            'Ch~04 DETERMINANTS',
            'Ch~05 CONTINUITY & DIFFERENTIABILITY',
            'Ch~06 APPLICATION OF DERIVATIVES',
            'Ch~07 INTEGRALS',
            'Ch~08 APPLICATION OF INTEGRALS',
            'Ch~09 DIFFERENTIAL EQUATIONS',
            'Ch~10 VECTOR ALGEBRA',
            'Ch~11 THREE DIMENSIONAL GEOMETRY',
            'Ch~12 LINEAR PROGRAMMING',
            'Ch~13 PROBABILITY'
        ],

        'SUB ~ GEOGRAPHY': [
            'Ch~01 HUMAN GEOGRAPHY : NATURE & SCOPE',
            'Ch~02 THE WORLD POPULATION',
            'Ch~03 POPULATION COMPOSITION',
            'Ch~04 HUMAN DEVELOPMENT',
            'Ch~05 PRIMARY ACTIVITIES',
            'Ch~06 SECONDARY ACTIVITIES',
            'Ch~07 TERTIARY & QUATERNARY ACTIVITIES',
            'Ch~08 TRANSPORT & COMMUNICATION',
            'Ch~09 INTERNATIONAL TRADE',
            'Ch~10 HUMAN SETTLEMENTS'
        ],

        'SUB ~ HISTORY': [
            'Ch~01 BRICKS, BEADS AND BONES',
            'Ch~02 KINGS, FARMERS AND TOWNS',
            'Ch~03 KINSHIP, CASTE AND CLASS',
            'Ch~04 THINKERS, BELIEFS AND BUILDINGS',
            'Ch~05 THROUGH THE EYES OF TRAVELLERS',
            'Ch~06 BHAKTI–SUFI TRADITIONS',
            'Ch~07 AN IMPERIAL CAPITAL : VIJAYANAGARA',
            'Ch~08 PEASANTS, ZAMINDARS AND THE STATE',
            'Ch~09 KINGS AND CHRONICLES',
            'Ch~10 COLONIALISM AND THE COUNTRYSIDE',
            'Ch~11 REBELS AND THE RAJ',
            'Ch~12 COLONIAL CITIES',
            'Ch~13 MAHATMA GANDHI AND THE NATIONALIST MOVEMENT',
            'Ch~14 UNDERSTANDING PARTITION',
            'Ch~15 FRAMING THE CONSTITUTION'
        ],

        'SUB ~ POLITY': [
            'Ch~01 THE CONSTITUTION : WHY AND HOW',
            'Ch~02 RIGHTS IN THE INDIAN CONSTITUTION',
            'Ch~03 ELECTION AND REPRESENTATION',
            'Ch~04 EXECUTIVE',
            'Ch~05 LEGISLATURE',
            'Ch~06 JUDICIARY',
            'Ch~07 FEDERALISM',
            'Ch~08 LOCAL GOVERNMENTS',
            'Ch~09 THE CONSTITUTION AS A LIVING DOCUMENT'
        ]
    }
}

#question load in question.json , this is for demo
load = {
"Ch~01" : [

["विद्युत आवेश का SI मात्रक क्या है?" , ["कूलाम" , "वोल्ट" , "एम्पियर" , "न्यूटन"] , "कूलाम"],

["समान आवेश एक-दूसरे के साथ क्या करते हैं?" , ["प्रतिकर्षण करते हैं" , "आकर्षण करते हैं" , "नष्ट हो जाते हैं" , "निष्क्रिय रहते हैं"] , "प्रतिकर्षण करते हैं"]
]
}

#==============================================

#Keyboard button creation
def buttons(btnName) :
    btns = btnName
    markup = types.ReplyKeyboardMarkup(row_width = 4 , resize_keyboard = True)
    all_button = []
    for button in btns :   
        btn = types.KeyboardButton(button)
        all_button.append(btn)
    markup.add(*all_button)
    return markup

#==============================================

#INLINE BUTTONS CREMATION
def inline_buttons(btnName):
    btns = btnName
    markup = types.InlineKeyboardMarkup(row_width=1 if any(len(btn) >= 10 for btn in btns ) else 3) 
    
    all_button = []    
    for button in btns : 
        btn = types.InlineKeyboardButton(button,callback_data = button)
        all_button.append(btn)
    
    markup.add(*all_button)
    return markup

#=============================================

#quiz sent func
def sent_quiz_poll(bot , chat_id , chapName) :
    if chat_id not in user_status :
        return
    load_que = load[chapName] #load quest according to chapter 
    que = random.choice(load_que) 
        
    #bot send poll func
    send_poll = bot.send_poll(
    chat_id = chat_id,
    question = que[0],
    options = que[1],
    type = "quiz",
    correct_option_id = que[1].index(que[2]),
    is_anonymous = False,
    open_period = 15)
        
    #bot repeat questions func
    threading.Timer(15.3, sent_quiz_poll, args=[bot, chat_id ,chapName]).start()

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
        res_button =buttons(['/weather','/quiz'])
        bot.send_message(message.chat.id , "👋🏻Hyy, I am weather bot.",reply_markup = res_button)

#==============================================
    
    #weather massage response 
    @bot.message_handler(func= lambda message :True if message=="weather" else False)
    def send_message1(message) :
        btns = buttons(indian_cities)
        bot.send_message(message.chat.id, "✍🏻Enter your city name.", reply_markup = btns)
     
#==============================================
    
    #weather details responser
    @bot.message_handler(func = lambda message : False if message == '/quiz' else True)
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
        if chat_id not in user_status :
            user_status[chat_id] = 'BOT ACTIVE'
            class_button = [ 'CLASS 12'] #all class button load in location file 
            all_btn = inline_buttons(class_button)
            bot.send_message(chat_id, 'Select your subject',reply_markup = all_btn)
            bot.send_message(chat_id, 'SORRY , This bot is working condition becasuse at present data are not available for bot\nIt is working only for class 12 → physics → Chapter 1\nI will all data for this bot early')
        else :
            bot.send_message(chat_id , 'you are already start quiz ')

#==============================================
           
    #CLASS handler    
    @bot.callback_query_handler(func = lambda call : call.data.startswith('CLASS'))
    def class_handler(call) :
        chat_id = call.message.chat.id
        bot.answer_callback_query(call.id)
        sub_list = list(location[call.data].keys()) #fatch all subjects in location file 
        all_btn = inline_buttons(sub_list)
        bot.send_message(chat_id, 'select you Subject', reply_markup = all_btn)
        bot_memory[chat_id] = call.data     
    
#==============================================
 
    #SUBJECT handler 
    @bot.callback_query_handler(func = lambda call : call.data.startswith('SUB ~ '))
    def subject_handler(call) :
        chat_id = call.message.chat.id
        bot.answer_callback_query(call.id)
        all_chap = list(location[bot_memory[chat_id]][call.data]
        ) #facth chapter's in location file
        all_btn = inline_buttons(all_chap)
        bot.send_message(chat_id , 'select you chapter', reply_markup = all_btn)
        
 #==============================================
       
    #CHAPTER handler  
    @bot.callback_query_handler(func = lambda call : call.data.startswith('Ch~'))
    def question(call) :
        chat_id = call.message.chat.id
        call_id = call.data[:5]
        bot.answer_callback_query(call.id)
#=========this condition for time limeted======= 
        if call.data == 'Ch~01 ELECTRIC CHARGES & FIELDS' :
            bot.send_message(chat_id, 'quiz start in 5 Sec')
            sent_quiz_poll(bot , chat_id , call_id)
        else :
            bot.send_message(chat_id, 'SORRY , This bot is working condition becasuse this time data are not available\nIt is working only for class 12 → physics → Chapter 1\nI am fixed this bot early')

#==============================================

    @bot.message_handler(commands = ["stop"])
    def stop_bot(message) :
        chat_id = message.chat.id
        if chat_id in user_status :
            user_name = message.from_user.first_name
            stop_text = (
                f"📌NOTICE📌\n\n"
                f"👤 QUIZ STOPPED by {user_name}.\n"
                f"✍🏻 If you want to restart quiz sent me /quiz")
            del user_status[chat_id]
            bot.send_message(chat_id , stop_text)
        else :
            pass
            
#=============================================

    keep_alive()
    print("Bot is running now .... ")
    bot.polling(none_stop = True,allowed_updates=["message", "poll", "poll_answer","callback_query"])
    
#==============================================

if __name__ == "__main__" :
    try :
        tegbot()
    except Exception as e :
        print(f"eroor as {e}")