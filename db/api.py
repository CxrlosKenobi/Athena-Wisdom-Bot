import pathlib
import sqlite3
#
from random import randint
#
from components.goodread import push

DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath('clips.db').resolve()

def getQuotesQuantity():
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  c.execute('SELECT COUNT(*) FROM clips')
  return c.fetchone()[0]


def getQuote():
  clippingsLength = getQuotesQuantity()
  seed = randint(0, clippingsLength - 1)
  push(id, False)

  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  c.execute('SELECT highlight, author, book FROM clips WHERE id = ?', (seed,))
  highlight, author, book = c.fetchone()

  return highlight, author, book


q = getQuote()
print(q)
