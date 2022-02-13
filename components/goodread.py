from telegram import ( InlineKeyboardButton, InlineKeyboardMarkup )
import pytz
#
from datetime import datetime
from random import randint
import json
#
from db.api import getQuotesQuantity


tz = pytz.timezone('America/Santiago')
dt = datetime.now(tz)

with open('data.json', 'r') as file:
  data = json.load(file)


def push(id, verified):
  if verified is True:
    with open('data/records.json', 'r') as file:
      hist = json.load(file)
      quotesLength = getQuotesQuantity()
      quotaLimit = round(quotesLength * 0.25)

      for i in range(quotaLimit + 1):
        if i < quotaLimit:
          hist[i] = hist[i + 1]
        else:
          hist[i] = id

      with open('data/records.json', 'w') as file:
        json.dump(hist, file, indent=2)
  else:
    with open('data/records.json', 'r') as file:
      hist = json.load(file)
      return hist


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
