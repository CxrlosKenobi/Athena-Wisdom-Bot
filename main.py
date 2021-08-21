from telegram.ext import Updater, CommandHandler
import telegram
import logging
import json
import datetime
from time import *
from random import randint

# Detect the token key on the json and import it
with open('token.json') as token_file:
    token = json.load(token_file)['token']

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

Clippings = []
# Formatting each highlight from clippings.txt
with open('Clippings.txt', 'r') as file:
    aux = 0
    unwanted = ['(', ')']
    for line in file:
        if aux == 0:
            # book = line[:line.find('(' or '-')] if line[:line.find('(' or '-')][-1] != ' ' else line[:line.find('(' or '-')][:-1]
            # author = line[line.find('('):]
            # for char in unwanted:
            #     author = author.replace(char, '')
            book, author = line, line
            aux += 1
        elif aux == 1:
            page, date = line, line
            aux += 1
        elif aux == 2:
            aux += 1
            continue
        elif aux == 3:
            highlight = line
            aux += 1
        elif aux == 4:
            out = {
                'book': book,
                'page': page,
                'author': author,
                'date': date,
                'highlight': highlight   
            }
            Clippings.append(out)
            aux = 0


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
        text="I'm a bot, please talk to me!")

def time(update, context):
    # Get the current time with the datetime library
    tiempo = datetime.datetime.now().strftime("%H:%M:%S")
    context.bot.send_message(chat_id=update.effective_chat.id, 
        text=tiempo)


def start_test(update, context):
    tiempo = datetime.datetime.now().strftime("%H:%M:%S")
    context.bot.send_message(chat_id=update.effective_chat.id,
        text=update["message"]["text"])

def quote(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
    text='Okay')
    while True:
        tiempo = datetime.datetime.now().strftime("%H:%M:%S")
        highlight = Clippings[randint(0, len(Clippings) - 1)]['highlight']
        if tiempo == '23:06:00':
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=highlight
            )
    
start_handler = CommandHandler('start', start)
time_handlder = CommandHandler('time', time)
start_test_handler = CommandHandler('start_test', start_test)
quote_handler = CommandHandler('quote', quote)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(time_handlder)
dispatcher.add_handler(start_test_handler)
dispatcher.add_handler(quote_handler)


# Start Diana
updater.start_polling()

