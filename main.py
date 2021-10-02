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
from components.college import *

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
    groupID = get['groupID']
    goodreadID = get['goodreadID']
    

updater = Updater(token=data["token"], use_context=True)
job_queue = updater.job_queue

def start(update, context):
    update.message.reply_text(
        "¡Hey, soy Diana the Wisdom Bot!\n\n"
        "Todo listo para comenzar ✅\n"
        "_Para obtener ayuda escribe /diana_"
    , parse_mode='Markdown')

def test(update, context):
    seed = randint(0, len(clippings)- 1)
    highlight = clippings[seed]['highlight']
    source = clippings[seed]['book']
    if len(source) < 3:
        source = clippings[seed]['author']

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text = f'_"{highlight}"_\n- *{source}*',
        parse_mode='Markdown'
    )

def Callback(context):
    seed = randint(0, len(clippings)- 1)
    highlight = clippings[seed]['highlight']
    source = clippings[seed]['book']

    # If book has no characters, use author instead
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
        msg = "🙁 ¡Oops! Please, try with a valid argument."
        context.bot.send_message(chat_id=goodreadID, text=msg)

        return 1

def greetThursday(context):
    with open('assets/jueves.gif', 'rb') as file:
        animated = file.read()
    context.bot.send_animation(groupID, animated)

def version(update, context):
    sourceCode = "https://github.com/CxrlosKenobi/Diana-Wisdom-Bot"
    update.message.reply_text(
        "<b>Diana Wisdom Bot v1.3\n</b>"
        f"<b>Código fuente: </b><a href='{sourceCode}'>GitHub</a>"
    , parse_mode="HTML")

def help(update, context):
    update.message.reply_text(
        """💻 *Comandos disponibles* 💻

• _/certs <rango> <ramoI, ramoII ...>_
• _/diana - Lista de comandos disponibles_
• _/version - Versión del bot y código fuente_
    """, parse_mode='Markdown')

def main():
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler('diana', help))
    dp.add_handler(CommandHandler('version', version))
    dp.add_handler(CommandHandler('certs', getSubjects, pass_args=True))

    dp.add_handler(CommandHandler('test', test))
    # dp.add_handler(CommandHandler('queue', displayJobQueue))
    job_queue = updater.job_queue
    job_queue.run_daily(
        greetThursday, 
        time=dt.replace(hour=8, minute=0, second=0, microsecond=0), 
        days=(3, ),
        name='Felíz Jueves'
    )


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
