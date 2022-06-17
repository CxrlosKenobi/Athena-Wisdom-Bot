from pymongo import MongoClient
from random import randint
#
from components.fetch import fetch_db_url

def connect():
  client = MongoClient(fetch_db_url)
  db = client.diana_wisdom
  collection = db.quotes

  return collection

def get_random_quote():
  collection = connect()
  _max = collection.count_documents({})
  _random = randint(1, _max)
  quote = collection.find_one({'id': _random})

  return quote


