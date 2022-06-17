import pathlib
import sqlite3
#
from random import randint
#
# from components.goodread import push

DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath('clips.db').resolve()

# def getQuotesQuantity():
#   conn = sqlite3.connect(DB_FILE)
#   c = conn.cursor()
#   c.execute('SELECT COUNT(*) FROM clips')
#   return c.fetchone()[0]


# def getQuote():
#   clippingsLength = getQuotesQuantity()
#   seed = randint(0, clippingsLength - 1)
#   push(id, False)

#   conn = sqlite3.connect(DB_FILE)
#   c = conn.cursor()
#   c.execute('SELECT highlight, author, book FROM clips WHERE id = ?', (seed,))
#   highlight, author, book = c.fetchone()

#   return highlight, author, book

def getAllInDicts():
  quotes = []
  conn = sqlite3.connect(DB_FILE)
  c = conn.cursor()
  c.execute('SELECT id, highlight, author, book, 0 FROM clips')
  for row in c.fetchall():
    source = {}
    if (row[2] == 'Quote') and (row[3] == ''):
      source = "None"
    elif (row[3] == '') and (row[2] != ''):
      source['author'] = row[2]
      source['bookAuthor'] = 'undefined'
      source['book'] = 'undefined'
    else:
      source['author'] = 'undefined'
      source['bookAuthor'] = [row[2]]
      source['book'] = row[3]

    quotes.append({
      'id': row[0],
      'quote': row[1],
      'source': source,
      'labels': []
    })

  return quotes    


# q = getQuote()
# print(q)
