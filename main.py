import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup

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
    
    bot.send_message(message.chat.id, f"Salom, {message.from_user.first_name}! Bot Render serverida 100% onlayn yangilandi! 🚀🌐", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    # 1. JONLI OB-HAVO
    if message.text == "🌤 Jonli Ob-havo":
        try:
            url = "https://wttr.in/Fergana?format=%c+%t+%C"
            response = requests.get(url, timeout=7)
            bot.reply_to(message, f"📍 Fargʻonada ayni vaqtdagi jonli ob-havo:\n\n{response.text} ☀️")
        except:
            bot.reply_to(message, "Ob-havo serverida uzilish bor. 🌤")
        
    # 2. FUTBOL YANGILIKLARI (HAQIQIY O'ZBEKCHA JONLI MANBA)
    elif message.text == "⚽️ Futbol Yangiliklari":
        try:
            url = "https://uzreport.news/feed/rss/uz/sports"
            response = requests.get(url, timeout=7)
            soup = BeautifulSoup(response.content, features="xml")
            items = soup.find_all('item')[:3]
            
            news_text = "⚽️ **UzReport tizimidan olingan jonli sport xabarlari:**\n\n"
            for item in items:
                title = item.title.text
                link = item.link.text
                news_text += f"📣 *{title}*\n🔗 [Batafsil o'qish]({link})\n\n"
            
            news_text += "🌍 (Xabarlar real vaqt rejimida internetdan yuklab olindi)"
            bot.send_message(message.chat.id, news_text, parse_mode="Markdown", disable_web_page_preview=True)
        except:
            bot.reply_to(message, "⚽️ Futbol serveri vaqtincha band, birozdan soʻng qayta bosing.")
        
    # 3. HAR XIL MAVZUDAGI JONLI FAKTLAR
    elif message.text == "💡 Qiziqarli Fakt":
        try:
            wiki_url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
            wiki_response = requests.get(wiki_url, timeout=7).json()
            title = wiki_response.get('title', '')
            extract = wiki_response.get('extract', '')
            combined_text = f"{title}: {extract}"
            
            translate_url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=uz&dt=t&q={combined_text[:500]}"
            translate_response = requests.get(translate_url, timeout=7).json()
            uzbek_fact = "".join([sentence[0] for sentence in translate_response[0]])
            
            bot.reply_to(message, f"💡 **Wikipedia'dan jonli ma'lumot (Mavzu: {title}):**\n\n{uzbek_fact}")
        except:
            bot.reply_to(message, "Fakt yuklashda muammo bo'ldi, qaytadan bosing. 💡")

bot.polling(none_stop=True)
