from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, 
    CommandHandler, 
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler
)
from datetime import datetime
from time import *
import logging
import json

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def getRemainingDays(subject):
    currentDate = datetime.now().strftime("%Y-%m-%d")
    subjectDate = subject['date']
    remainingDays = (datetime.strptime(subjectDate, "%Y-%m-%d") - datetime.strptime(currentDate, "%Y-%m-%d")).days

    return remainingDays

# Telegram command that returns each subject with its remaining days
def getSubjects(update, context):
    with open('Udec.json') as file:
        data = json.load(file)

    msgUsage = """
⚠️ ¡Asegúrate de seguir el formato!
      /pruebas <Rango> <Ramo, ramo ...>    
"""

    try:
        rango = int(context.args[0])
        if rango > 120:
            rango = 120
    except (IndexError, ValueError):
        rango = 31

    try:
        if not (context.args[0].isdigit()):
            print()






        if not context.args[0].isdigit():
            if len(context.args) > 1:
                ramos = context.args[0].split(',')
                if context.args[0].isdigit():
                    update.message.reply_text(msgUsage)
            else:
                ramos = [context.args[0]]
        else:
            if len(context.args) > 2:
                ramos = context.args[1].split(', ')
                if context.args[1:].isdigit():
                    update.message.reply_text(msgUsage)

            else:
                ramos = [context.args[1]]
                if context.args[1:].isdigit():
                    update.message.reply_text(msgUsage)
    except IndexError:
        ramos = []
    
    print(ramos)
    print(type(ramos))
    


    subjectsList = []
    for subject in data:
        if getRemainingDays(subject) > rango:
            continue
        subjectsList.append(f"{getRemainingDays(subject)} días - {subject['name']}")
    subjectsList.sort(key=lambda x: int(x.split(' ')[0]))    

    body = f"""
    ✳️ *Próximos certámenes* ✳️
~ Rango: {rango} días

"""

    status = ['🔴', '🟠', '🟡', '🟢']
    for subject in subjectsList:
        remaining = int(subject.split(' ')[0])
        if 0 <= remaining <= 7 :
            assignedStatus = status[0]
        elif 8 <= remaining <= 14:
            assignedStatus = status[1]
        elif 15 <= remaining <= 20:
            assignedStatus = status[2]
        else:
            assignedStatus = status[3]

        body += f"• {assignedStatus} _{subject}_\n"

    update.message.reply_text(body, parse_mode='Markdown')


def main():
    with open('token.json') as token_file:
        token = json.load(token_file)['token']

    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('pruebas', getSubjects, pass_args=True))
    # dp.add_handler(CommandHandler('pruebas', getSubjects))

    print('[ ! ] Initializing bot ...')
    updater.start_polling()
    print('[ ok ] Bot is running ...')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n[ ! ] Exiting ...')
        exit(1)
