import telebot #Библиотека для бота
from telebot import types
import telegram

bot = telebot.TeleBot(' APIKEY ') #===АПИ токен бота===

@bot.message_handler(func=lambda message: message.text == "Дай мой ИД")
def get_id_chat(message):
    bot.send_message(message.chat.id, message.chat.id)

bot.infinity_polling()