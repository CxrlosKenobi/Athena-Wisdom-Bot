from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from datetime import datetime
import pytz
import json
from random import randint
from random import random

tz = pytz.timezone('America/Santiago')
dt = datetime.now(tz)

with open('data.json', 'r') as file:
    data = json.load(file)


def push(highlight, verified):
    if verified is True:
        authors = {}
        with open('data/records.json', 'r') as file:
            hist = json.load(file)

            # for i in range(len(hist)):
            #     if hist.author in authors:
            #         authors[hist.author][0] += 1
            #     else:
            #         authors[hist.author] = [1, hist.highlight]

            # authors.sort(reverse=True)

            # for i in authors:
            #     n = random()
            #     if n < authors[i]:
            #         clipping = authors[i][1]

            quotaLimit = 15  # Calcular porcentaje
            for i in range(quotaLimit + 1):
                if i < quotaLimit:
                    hist[i] = hist[i+1]
                else:
                    hist[i] = highlight

            with open('data/records.json', 'w') as file:
                json.dump(hist, file, indent=4)
    else:
        with open('data/records.json', 'r') as file:
            hist = json.load(file)
            return hist


def btnMode(update, context):
    update.message.reply_text(
        text='Type something...',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Morning Mode',
                                  callback_data='morning')],
            [InlineKeyboardButton(text='Noon Mode', callback_data='noon')],
            [InlineKeyboardButton(text='Night Mode', callback_data='night')]
        ])
    )


def morningMode():
    h = randint(7, 11)
    m = randint(0, 60)

    name = 'Have a good read at morning!'
    days = (0, 1, 2, 3, 4, 5, 6)
    time = dt.replace(hour=h, minute=m, second=0, microsecond=0)

    return time, days, name


def noonMode():
    h = randint(13, 18)
    m = randint(0, 60)

    name = 'Have a good read at noon!'
    days = (0, 1, 2, 3, 4, 5, 6)
    time = dt.replace(hour=h, minute=m, second=00, microsecond=0)

    return time, days, name


def nightMode():
    h = randint(20, 22)
    m = randint(0, 60)

    name = 'Have a good read at night!'
    days = (0, 1, 2, 3, 4, 5, 6)
    time = dt.replace(hour=h, minute=m, second=0, microsecond=0)

    return time, days, name
