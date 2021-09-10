from telegram.ext import (Updater, 
    CommandHandler, 
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

def start(update, context):
    update.message.reply_text(
        "¡Hey, soy Diana the Wisdom Bot!\n\n"
        "Todo listo para comenzar ✅\n"
        "_Para obtener ayuda escribe /diana_"
    , parse_mode='Markdown')

def version(update, context):
    sourceCode = "https://github.com/CxrlosKenobi/Diana-Wisdom-Bot"
    update.message.reply_text(
        "<b>Diana Wisdom Bot v1.1\n</b>"
        f"<b>Código fuente: </b><a href='{sourceCode}'>GitHub</a>"
    , parse_mode="HTML")


def help(update, context):
    update.message.reply_text(
        """💻 *Comandos disponibles* 💻

• _/certs <rango> <ramoI, ramoII ...>_
• _/help - Lista de comandos disponibles_
• _/version - Versión del bot y código fuente_
    """, parse_mode='Markdown')

def getRemainingDays(subject):
    currentDate = datetime.now().strftime("%Y-%m-%d")
    subjectDate = subject['date']
    remainingDays = (datetime.strptime(subjectDate, "%Y-%m-%d") - datetime.strptime(currentDate, "%Y-%m-%d")).days

    return remainingDays

def getSubjects(update, context):
    with open('Udec.json') as file:
        data = json.load(file)

    alertMsg = """
⚠️ ¡Asegúrate de seguir el formato!
      _/pruebas <rango> <ramoI, ramoII ...>_
"""
    noneMsg = """
🙁 ¡Oops! No poseo asignaturas llamadas así.
"""
    try:
        if context.args[0] == 'help':
            update.message.reply_text(alertMsg, parse_mode='Markdown')
            return
    except IndexError:
        pass

    try:
        rango = int(context.args[0])
        if rango > 120:
            rango = 120
    except (IndexError, ValueError):
        rango = 31

    try:
        if not (context.args[0].isdigit()):
            ramosRaw = context.args

        elif (context.args[0].isdigit()):
            if len(context.args) > 1:
                ramosRaw = context.args[1:]
            elif len(context.args) == 1:
                ramosRaw = []
        else:
            update.message.reply_text(alertMsg)
            return
        

    except IndexError:
        ramosRaw = []
    
    ramos = []
    for j in ramosRaw:
        try:
            if (j[-1] == 'I') and (j[-2] == 'I'):
                j = j.replace('II', ' II')
                ramos.append(j.lower())
            elif (j[-1] == 'I') and (j[-2] != 'I'):
                j = j.replace('I', ' I')
                ramos.append(j.lower())

            elif (j[-1] == 'i') and (j[-2] == 'i'):
                j = j.replace('ii', ' ii')
                ramos.append(j.lower())
            elif (j[-1] == 'i') and (j[-2] != 'i'):
                j = j.replace('i', ' i')
                ramos.append(j.lower())
            else:
                ramos.append(j.lower())
                pass
        except IndexError:
            ramos.append(j.lower())
            pass

    subjectsList = []
    for subject in data:
        if getRemainingDays(subject) > rango:
            continue
        if ramos:
            if subject['name'].lower() in ramos:
                subjectsList.append(f"{getRemainingDays(subject)} días - {subject['name']}")
            else:
                continue
        else:
            subjectsList.append(f"{getRemainingDays(subject)} días - {subject['name']}")
    if subjectsList == []:
        update.message.reply_text(noneMsg)
        return
    else:
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
        elif 15 <= remaining <= 23:
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

    dp.add_handler(CommandHandler('diana', help))
    dp.add_handler(CommandHandler('version', version))
    dp.add_handler(CommandHandler('certs', getSubjects, pass_args=True))
    dp.add_handler(CommandHandler('start', start))


    print('[ ! ] Initializing bot ...')
    updater.start_polling()
    print('[ ok ] Bot is running ...')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n[ ! ] Exiting ...')
        exit(1)
