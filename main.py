import telebot
from telebot import types
import requests

TOKEN = '8823313746:AAGPCuC9KnsKWuokZqjsEaXAIeUaj56vCEc'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_weather = types.KeyboardButton("🌤 Jonli Ob-havo")
    btn_football = types.KeyboardButton("⚽️ Futbol Yangiliklari")
    btn_fact = types.KeyboardButton("💡 Qiziqarli Fakt")
    markup.add(btn_weather, btn_football)
    markup.add(btn_fact)
    
    bot.send_message(message.chat.id, f"Salom, {message.from_user.first_name}! Yangi serverga xush kelibsiz. Endi hamma narsa 100% jonli va erkin! 🌍", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    # 1. JONLI OB-HAVO
    if message.text == "🌤 Jonli Ob-havo":
        try:
            url = "https://wttr.in/Fergana?format=%c+%t+%C"
            response = requests.get(url, timeout=5)
            bot.reply_to(message, f"📍 Fargʻonada ayni vaqtdagi jonli ob-havo:\n\n{response.text} ☀️")
        except:
            bot.reply_to(message, "Ob-havo tizimida uzilish bor. 🌤")
        
    # 2. FUTBOL YANGILIKLARI (HAQIQIY INTERNETDAN)
    elif message.text == "⚽️ Futbol Yangiliklari":
        try:
            # Global futbol bazasidan eng qaynoq yangiliklarni onlayn yuklash
            url = "https://raw.githubusercontent.com/jamesacampbell/football-data/master/news.json"
            response = requests.get(url, timeout=5).json()
            
            news_text = "⚽️ **Dunyo futbolidagi eng soʻnggi onlayn xabarlar:**\n\n"
            
            for item in response[:3]: # Eng oxirgi 3 ta yangilik
                eng_title = item.get('title', '') or item.get('heading', '')
                if eng_title:
                    # Inglizcha yangilikni Google orqali onlayn o'zbekcha qilish
                    tr_url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=uz&dt=t&q={eng_title}"
                    tr_res = requests.get(tr_url, timeout=5).json()
                    uz_title = "".join([sentence[0] for sentence in tr_res[0]])
                    news_text += f"📣 {uz_title}\n\n"
            
            bot.send_message(message.chat.id, news_text)
        except:
            bot.reply_to(message, "Futbol serverida muammo bo'ldi. ⚽️")
        
    # 3. QIziqarli FAKT (HAQIQIY INTERNETDAN)
    elif message.text == "💡 Qiziqarli Fakt":
        try:
            # Dunyo faktlar omboridan tasodifiy mutlaqo yangi fakt olish
            fact_url = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
            fact_response = requests.get(fact_url, timeout=5).json()
            english_fact = fact_response['text']
            
            # Uni o'sha soniyada o'zbekchaga o'girish
            translate_url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=uz&dt=t&q={english_fact}"
            translate_response = requests.get(translate_url, timeout=5).json()
            uzbek_fact = "".join([sentence[0] for sentence in translate_response[0]])
            
            bot.reply_to(message, f"💡 **Internetdan olingan jonli fakt:**\n\n{uzbek_fact}")
        except:
            bot.reply_to(message, "Fakt yuklashda uzilish bo'ldi. 💡")

bot.polling(none_stop=True)
