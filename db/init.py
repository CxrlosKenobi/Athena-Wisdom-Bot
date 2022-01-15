import os
import sqlite3
import configparser
from sqlalchemy import Table
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

config = configparser.ConfigParser()
config.read('config.txt')
engine = create_engine(config.get('database', 'con'))

conn = sqlite3.connect('clips.db')
cur = conn.cursor()
print('[ ok ] Database connected!')

cur.execute(
"""
CREATE TABLE IF NOT EXISTS clips (
  id INTEGER,
  book VARCHAR(40),
  author VARCHAR(40),
  page VARCHAR(40),
  date VARCHAR(40),
  highlight VARCHAR(255),
  UNIQUE (id),
  PRIMARY KEY (id)
);
"""
)
conn.commit()
cur.close()
print('[ ok ] Clips table has been created!')

db = SQLAlchemy()

class Clips(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    book = db.Column(db.String(40))
    author = db.Column(db.String(40))
    page = db.Column(db.String(40))
    date = db.Column(db.String(40))
    highlight = db.Column(db.String(255))
  
Clip_tbl = Table('clips', Clips.metadata)
def create_data_table():
  Clips.metadata.create_all(engine)

def add_data(id, book, author, page, date, highlight):
  ins = Clip_tbl.insert().values(
    id=id,
    book=book,
    author=author,
    page=page,
    date=date,
    highlight=highlight
  )
  conn = engine.connect()
  conn.execute(ins)
  conn.close()


# Loading data into the database
clippings = []
with open('../data/clippings.txt') as file:
  unwanted = ['(', ')', '"', '«', '»']
  row = 0
  for line in file:
    if row == 0: # Book & Author
      if '-' in line:
        line = line.split(' - ')
        book = line[0].strip()
        author = line[1].strip()
      elif '(' in line:
        line = line.split('(')
        book = line[0].strip()
        author = line[1].strip()
        author = author.split(')')[0]
      else:
        book, author = line, line            
      row += 1

    elif row == 1: # Highlight page and date
      page, date = line, line
      # line = line.split('|')
      # page = line[0].strip().split(' ')[-1].split('-')[-1]            
      # date = line[1].strip()
      row += 1
    elif row == 2: # Empty line
      row += 1
      continue
    elif row == 3: # Highlight
      highlight = line
      for char in unwanted:
        highlight = highlight.replace(char, '')

      highlight = (highlight[0].upper() + highlight[1:]).strip()
      if highlight[-1] == '.':
        pass
      else:
        highlight = highlight + '.'
      row += 1
    elif row == 4: # Separator and end of clipping
      # Give the id a unique value for the clip
      out = {
        'id': len(clippings) + 1,
        'book': book,
        'page': page,
        'author': author,
        'date': date,
        'highlight': highlight   
      }
      clippings.append(out)
      row = 0

print('[ ok ] Clippings loaded!')

# Save the clippings to the database
for clip in clippings:
  add_data(
    int(clip['id']),
    clip['book'],
    clip['author'],
    clip['page'],
    clip['date'],
    clip['highlight']
  )
  print(f"[ ok ] Clip n°{clip['id']} added to database!")

  
# from pprint import pprint 
# pprint(clippings)
