from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, 
    CommandHandler, 
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler
)
from datetime import datetime
from random import randint
from time import *
import logging
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

Clippings = []
# Formatting each highlight from clippings.txt
with open('Clippings.txt') as file:
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


def set_time(update, context, t):
    userMessage = str(update.message.text)
    for char in range(len(userMessage)):
        if userMessage[char] == " ":
            userMessage = userMessage[char+1:]
            break
    if userMessage == "/greeting":
        userMessage = ""
            
    now = datetime.now()
    ctime = now.strftime("%H:%M:%S")

    if ctime == userMessage:
        highlight = Clippings[randint(0, len(Clippings) - 1)]['highlight']
        context.bot.send_message(chat_id=update.effective_chat.id, text=highlight)

def callback(update, context):
    highlight = Clippings[randint(0, len(Clippings) - 1)]['highlight']
    context.bot.send_message(chat_id=update.effective_chat.id, text=highlight)

period = []
def set(update, context):
    userMessage = str(update.message.text)
    for char in range(len(userMessage)):
        if userMessage[char] == " ":
            userMessage = userMessage[char+1:]
            period.append(userMessage)
            break
    
    if userMessage == "/greeting":
        userMessage = ""

def time(update, context):
    context.job_queue.run_repeating(
        callback,
        if datetime.now()strftime("%H:%M:%S") in period, # seconds
        context=update.message.chat_id
    )

    
def greeting(update, context):
    userMessage = str(update.message.text)
    for char in range(len(userMessage)):
        if userMessage[char] == " ":
            userMessage = userMessage[char+1:]
            break
        
    context.bot.send_message(chat_id=update.effective_chat.id, 
        text=userMessage)


def main():
    with open('token.json') as token_file:
        token = json.load(token_file)['token']
    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('greeting', greeting))
    dp.add_handler(CommandHandler('set_time', set_time))

    print('[ ! ] Initializing bot ...')
    updater.start_polling()
    print('[ ok ] Bot is running ...')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n[ ! ] Exiting ...')
        exit(1)
