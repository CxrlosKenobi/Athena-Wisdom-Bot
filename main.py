from telegram.ext import (
    Updater, 
    CommandHandler, 
    MessageHandler, 
    Filters, 
    ConversationHandler,
    CallbackQueryHandler
)
from random import randint
import logging
import json

from components.formatting import Clip
from components.goodread import *

INPUT_TEXT = 0
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)
clippings = Clip()


with open('data.json', 'r') as file:
    get = json.load(file)
    token = get['token']
    goodreadID = get['goodreadID']
    

updater = Updater(token=data["token"], use_context=True)
job_queue = updater.job_queue

def start(update, context):
    update.message.reply_text(
        "¡Hey, I'm Diana the Wisdom Bot!\n\n"
        "Everything ready to start! ✅\n"
        "_For more help, type /diana_"
    , parse_mode='Markdown')    

def get(update, context):
    seed = randint(0, len(clippings)- 1)
    highlight = clippings[seed]['highlight']
    author = clippings[seed]['author']
    history = push(author, False)

    doWhile = True
    while doWhile == True:
        if highlight in list(history.values()):
            seed = randint(0, len(clippings)- 1)
            highlight = clippings[seed]['highlight']
            doWhile = True
        elif highlight not in list(history.values()):
            source = clippings[seed]['book']
            doWhile = False
        else:
            print('\n[ * ] Cycles error at Callback')
            return exit(1)

    history = push(author, True)
    if len(source) < 3:
        source = clippings[seed]['author']

    update.message.reply_text(
        # chat_id=update.effective_chat.id,
        text = f'_"{highlight}"_\n- *{source}*',
        parse_mode='Markdown'
    )

def Callback(context):
    seed = randint(0, len(clippings)- 1)
    highlight = clippings[seed]['highlight']
    author = clippings[seed]['author']
    history = push(author, False)

    doWhile = True
    while doWhile == True:
        if author in list(history.values()):
            seed = randint(0, len(clippings)- 1)
            highlight = clippings[seed]['highlight']
            doWhile = True
        elif author not in list(history.values()):
            doWhile = False
            source = clippings[seed]['book']
        else:
            print('\n[ * ] Cycles error at Callback')
            return exit(1)

    history = push(author, True)
        
    if len(source) < 3:
        source = clippings[seed]['author']

    context.bot.send_message(
        chat_id=goodreadID, 
        text = f'_"{highlight}"_\n- *{source}*',
        parse_mode='Markdown'
    )

def run_daily(time, days, name):
    job_queue.run_daily(
        Callback,
        time=time,
        days=days,
        name=name
    )


def Sched(update, context):
    query = update.callback_query
    if query.data == 'morning':
        time, days, name = morningMode()
        run_daily(time, days, name)
        query.edit_message_text(
            text=f'Morning mode is set to run at {time.strftime("%H:%M:%S")}'
        )

    elif query.data == 'noon':
        time, days, name = noonMode()
        run_daily(time, days, name)
        query.edit_message_text(
            text=f'Noon mode is set to run at {time.strftime("%H:%M:%S")}'
        )

    elif query.data == 'night':
        time, days, name = nightMode()
        run_daily(time, days, name)
        query.edit_message_text(
            text=f'Night mode is set to run at {time.strftime("%H:%M:%S")}'
        )

    else:
        msg = "🙁 ¡Oops! Please, try with doWhile valid argument."
        context.bot.send_message(chat_id=goodreadID, text=msg)

        return 1


def version(update, context):
    sourceCode = "https://github.com/CxrlosKenobi/Diana-Wisdom-Bot"
    update.message.reply_text(
        "<b>Diana Wisdom Bot v1.4</b> \n"
        f"<b>Source code: </b><a href='{sourceCode}'>GitHub</a>"
    , parse_mode="HTML")

def help(update, context):
    update.message.reply_text(
        """💻 *Supported Commands* 💻

• _/get - Inspirational quotes_
• _/sched - Set schedule for quotes_
• _/diana - Displays supported commands_
• _/version - Bot version & Source code_
    """, parse_mode='Markdown')

def main():
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler('diana', help))
    dp.add_handler(CommandHandler('version', version))

    dp.add_handler(CommandHandler('get', get))
    # dp.add_handler(CommandHandler('queue', displayJobQueue))
    job_queue = updater.job_queue

    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('sched', btnMode),
            CallbackQueryHandler(Sched)
        ],

        states={
            INPUT_TEXT: [MessageHandler(Filters.text, Sched)]
        },

        fallbacks=[CommandHandler('cancel', btnMode)]
    ))

    print('[ ! ] Initializing bot ...')
    updater.start_polling()
    print('[ ok ] Bot is running ...')
    updater.idle()

if __name__ == '__main__':
    main()
