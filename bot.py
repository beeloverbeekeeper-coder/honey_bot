import os
import telebot
from openai import OpenAI

BOT_TOKEN = os.environ.get('BOT_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """შენ ხარ პირადი AI კოუჩი. შენი მომხმარებელი არის მეფუტკრე საქართველოდან, 
რომელსაც აქვს 15 ტონა თაფლი და სურს $1,000,000 გამომუშავება. 
ყოველდღე დაეხმარე "The One Thing" პრინციპით - იკითხე რა არის ერთი ყველაზე მნიშვნელოვანი რამ 
რასაც დღეს უნდა გააკეთოს მიზნისკენ. იყავი მოტივატორი, კონკრეტული და პრაქტიკული."""

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "გამარჯობა! მე ვარ შენი პირადი AI კოუჩი 🐝\n\nდღეს რა არის ის ერთი რამ რასაც გააკეთებ მიზნისკენ?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message.text}
        ]
    )
    bot.reply_to(message, response.choices[0].message.content)

bot.polling()
