from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from datetime import datetime
from .formatting import Clip
import pytz
import json

tz = pytz.timezone('America/Santiago')
dt = datetime.now(tz)

with open('data.json', 'r') as file:
    data = json.load(file)

def btnMode(update, context):
    update.message.reply_text(
        text='Type something...',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Morning Mode', callback_data='morning')],
            [InlineKeyboardButton(text='Noon Mode', callback_data='noon')],
            [InlineKeyboardButton(text='Night Mode', callback_data='night')]
        ])
    )


def morningMode():
    name = 'Have a good read at morning!'
    days = (0, 1, 2, 3, 4, 5, 6)
    time = dt.replace(hour=8, minute=45, second=0, microsecond=0)
    
    return time, days, name

def noonMode():
    name = 'Have a good read at noon!'
    days = (0, 1, 2, 3, 4, 5, 6)
    time = dt.replace(hour=17, minute=21, second=00, microsecond=0)

    return time, days, name

def nightMode():
    name = 'Have a good read at night!'
    days = (0, 1, 2, 3, 4, 5, 6)
    time = dt.replace(hour=21, minute=30, second=0, microsecond=0)

    return time, days, name
