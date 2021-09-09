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
import telegramcalendar
from time import *
import logging
import json

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

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

NAME, TIME_Q, INFO, OPT = range(4)
def json_editor(user, key, value):
    user = str(user)
    with open("reminder.json", "r+") as file:
        content = json.load(file)
        if user not in content["reminder"].keys():
            content["reminder"][user] = {"utc": 0, "reminder": []}
        if key == "name":
            content["reminder"][user]["reminder"].insert(0, {})
        content["reminder"][user]["reminder"][0][key] = value
        file.seek(0)
        json.dump(content, file)
        file.truncate()


def json_getter(user, ):
    with open("reminder.json") as file:
        content = json.load(file)
        element = content["reminder"][user]["reminder"][0]
        name = element["name"]
        _time = element["time"]
        r_id = element["id"]
        return name, date, _time, r_id


def json_deleter(user, r_id=None, current=False):
    with open("reminder.json", "r+") as file:
        content = json.load(file)
        reminder = content["reminder"][user]["reminder"]
        if not current:
            for i in range(len(reminder)):
                if reminder[i]["id"] == r_id:
                    del reminder[i]
                    break
        else:
            del reminder[0]
        file.seek(0)
        json.dump(content, file)
        file.truncate()


def all_reminder(update, context):
    reply_keyboard = [["/start", "/list", "/time"]]
    username = str(update.message["chat"]["id"])
    with open("reminder.json") as file:
        content = json.load(file)
        reminder = content["reminder"][username]["reminder"]
        if len(reminder) == 0:
            update.message.reply_text(f"\U0001F4C3 *Reminder List* \U0001F4C3\n\nYou don't have any reminders saved!", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True), parse_mode="markdown")
        else:
            update.message.reply_text("\U0001F4CB* Reminder List *\U0001F4CB", parse_mode="markdown")
            for i, v in enumerate(reminder):
                name = v["name"]
                _time = v["time"]
                if "opt_inf" in v.keys():
                    information = v["opt_inf"]
                    if i == len(reminder) - 1:
                        update.message.reply_text(f"{i+1}:   Appointment: {name}\n      Time: {_time}\n      Information: {information}", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
                    else:
                        update.message.reply_text(f"{i+1}:   Appointment: {name}\n      Time: {_time}\n      Information: {information}")
                else:
                    if i == len(reminder) - 1:
                        update.message.reply_text(f"{i+1}:   Appointment: {name}\n      Time: {_time}", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
                    else:
                        update.message.reply_text(f"{i+1}:   Appointment: {name}\n      Time: {_time}")


def notification(context):
    reply_keyboard = [["/start", "/list", "/time"]]
    job = context.job
    if len(job.context) == 5:
         name, _time, username, r_id = job.context[1], job.context[2], job.context[3], job.context[4], job.context[5]
         context.bot.send_message(job.context[0], text=f"\U0001F4A1* Reminder *\U0001F4A1\n\nAppointment: {name}\nScheduled for {_time}.\nThe appointment starts in 10 minutes!", parse_mode="markdown")
    else:
        name, _time, username, r_id, information = job.context[1], job.context[2], job.context[3], job.context[4], job.context[5], job.context[6]
        context.bot.send_message(job.context[0], text=f"\U0001F4A1* Reminder *\U0001F4A1\n\nAppointment: {name}\nInformation: {information}\n\nScheduled for {_time}.\nThe appointment starts in 10 minutes!", parse_mode="markdown", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
    json_deleter(username, r_id=r_id)

def start(update, context):
    # print(update.message)
    update.message.reply_text("*\U0001F4CD Reminder Setup *\U0001F4CD\n\nWhat should be the name\nof the appointment?", parse_mode="markdown")
    # update.message.reply_text(f"test", reply_markup=telegramcalendar.create_clock(), parse_mode="markdown")
    return NAME

def name(update, context):
    name = update.message.text
    if name == "/cancel":
        cancel(update, context)
        return ConversationHandler.END
    username = update.message["chat"]["id"]
    json_editor(username, "name", name)
    logger.info("Name: %s", update.message.text)
    update.message.reply_text(f"\U0001F4C5* Reminder Setup *\U0001F4C5\n\nWhen do you want to be\nreminded for *{name}*?",
                              reply_markup=telegramcalendar.create_calendar(), parse_mode="markdown")
    return DATE_Q


def inline_handler(update, context):
    selected, _time = telegramcalendar.process_clock_selection(context.bot, update)
    if selected:
        chat_id = str(update.callback_query.from_user.id)
        r_id = randint(0, 100000)
        format_time = f"{_time[0]}:{_time[1]} {_time[2]}"
        json_editor(chat_id, "time", format_time)
        json_editor(chat_id, "id", r_id)

        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=f"You selected {format_time}",
                                 reply_markup=ReplyKeyboardRemove())
        reply_keyboard = [["Yes", "No"]]
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                text=f"\U0001F530 *Reminder Setup* \U0001F530\n\nDo you want to add an\ninformation to the reminder?",
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True), parse_mode="markdown")
        return INFO


def info(update, context):
    text = update.message.text
    if text == "Yes":
        update.message.reply_text(f"\U00002139 *Reminder Setup* \U00002139\n\nSend the additional information\nyou want to be added to your reminder!", parse_mode="markdown")
        return OPT
    else:
        reply_keyboard = [["/start", "/list", "/time"]]
        chat_id = str(update.message["chat"]["id"])
        name, format_time, r_id = json_getter(chat_id)
        hour, minute, m = int(format_time.split(" ")[0].split(":")[0]), int(format_time.split(" ")[0].split(":")[1]), format_time.split(" ")[1]

        if "pm" in m:
            n_hour = hour + 12
        else:
            n_hour = hour

        context.bot.send_message(chat_id=chat_id,
                                    text=f"*\U0001F4CC Saved Reminder *\U0001F4CC\n\nAppointment: {name}\nDate: {date}\nTime: {hour}:{minute} {m}",
                                    parse_mode="markdown",
                                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                    resize_keyboard=True))
        context.job_queue.run_once(notification, seconds, context=[chat_id, name, date, format_time, chat_id, r_id], name=chat_id)
        return ConversationHandler.END

def opt_info(update, context):
    reply_keyboard = [["/start", "/list", "/time"]]
    information = update.message.text
    chat_id = str(update.message["chat"]["id"])
    json_editor(chat_id, "opt_inf", information)
    name, format_time, r_id = json_getter(chat_id)
    hour, minute, m = int(format_time.split(" ")[0].split(":")[0]), int(format_time.split(" ")[0].split(":")[1]), format_time.split(" ")[1]

    if "pm" in m:
        n_hour = hour + 12
    else:
        n_hour = hour
    seconds = timedelta(hours=n_hour, minutes=minute) - (datetime.timestamp(datetime.now()) + (num * 3600))
    context.bot.send_message(chat_id=chat_id,
                                text=f"*\U0001F4CC Saved Reminder *\U0001F4CC\n\nAppointment: {name}\nTime: {hour}:{minute} {m}",
                                parse_mode="markdown",
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                resize_keyboard=True))
    context.job_queue.run_once(notification, seconds, context=[chat_id, name, format_time, chat_id, r_id, information], name=chat_id)
    return ConversationHandler.END

def cancel(update, context):
    username = str(update.message["chat"]["id"])
    logger.info("User %s canceled the reminder setup.", username)
    json_deleter(username, current=True)
    update.message.reply_text('\U0001F53A *Reminder Setup* \U0001F53A'
                              '\n\nYou canceled the reminder!', reply_markup=ReplyKeyboardRemove(), parse_mode="markdown")
    return ConversationHandler.END




def phrase(update, context):
    highlight = Clippings[randint(0, len(Clippings) - 1)]['highlight']
    context.bot.send_message(chat_id=update.effective_chat.id, text=highlight)

def set_time(update, context):

    userMessage = str(update.message.text)
    for char in range(len(userMessage)):
        if userMessage[char] == " ":
            userMessage = userMessage[char+1:]
            break
    now = datetime.now()
    ctime = now.strftime("%H:%M:%S")

    if ctime == userMessage:
        highlight = Clippings[randint(0, len(Clippings) - 1)]['highlight']
        context.bot.send_message(chat_id=update.effective_chat.id, text=highlight)
    else:
        s1 = userMessage
        s2 = ctime
        FMT = '%H:%M:%S'
        tdelta = datetime.strptime(s1, FMT) - datetime.strptime(s2, FMT)
        sleep((tdelta.seconds))
        highlight = Clippings[randint(0, len(Clippings) - 1)]['highlight']
        context.bot.send_message(chat_id=update.effective_chat.id, text=highlight)
        
    context.job_queue.run_repeating(phrase, 5, context=update.message.chat_id)

def greeting(update, context):
    userMessage = str(update.message.text)
    for char in range(len(userMessage)):
        if userMessage[char] == " ":
            userMessage = userMessage[char+1:]
            break
        
    context.bot.send_message(chat_id=update.effective_chat.id, 
        text=userMessage)
        
    # context.bot.send_message(context.job.context, text="S.O.S.", reply_markup=clock.create_clock(user=update.callback_query.from_user.id))

def callback(context):
    highlight = Clippings[randint(0, len(Clippings) - 1)]['highlight']
    context.bot.send_message(context.job.context, text=highlight)

def time(update, context):
    context.job_queue.run_repeating(
        callback,
        10, # seconds
        context=update.message.chat_id
    )

def main():
    with open('token.json') as token_file:
        token = json.load(token_file)['token']
    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher

    all_reminder_handler = CommandHandler("list", all_reminder)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text, name)],
            TIME_Q: [CallbackQueryHandler(inline_handler)],
            INFO: [MessageHandler(Filters.text, info)],
            OPT: [MessageHandler(Filters.text, opt_info)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(all_reminder_handler)
    dp.add_handler(CommandHandler('greeting', greeting))
    dp.add_handler(CommandHandler('set_time', set_time))
    dp.add_handler(CommandHandler('phrase', phrase))

    print('[ ! ] Initializing bot ...')
    updater.start_polling()
    updater.idle()

    print('[ ok ] Bot is running ...')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n[ ! ] Exiting ...')
        exit(1)

    # else:
    #     s1 = userMessage
    #     s2 = ctime
    #     FMT = '%H:%M:%S'
    #     tdelta = datetime.strptime(s1, FMT) - datetime.strptime(s2, FMT)
    #     sleep((tdelta.seconds))
    #     highlight = Clippings[randint(0, len(Clippings) - 1)]['highlight']
    #     context.bot.send_message(chat_id=update.effective_chat.id, text=highlight)
        
    # context.job_queue.run_repeating(phrase, 5, context=update.message.chat_id)
