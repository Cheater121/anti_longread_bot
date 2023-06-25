import telebot
from environs import Env

env: Env = Env()
env.read_env()

bot = telebot.TeleBot(env('ALR_TOKEN'))


@bot.message_handler(is_chat_admin=True, commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id,
                     "Hi, i will protect you from long-reads")


@bot.message_handler(func=lambda message: message.forward_from_chat and len(message.text) > 500)
def handle_long_message(message):
    # Delete the long forwarded message
    bot.delete_message(message.chat.id, message.message_id)
    # Send the link to the original message
    original_link = f"https://t.me/{message.forward_from_chat.username}/{message.forward_from_message_id}"
    bot.send_message(message.chat.id, original_link)


bot.polling()
