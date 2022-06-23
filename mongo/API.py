from pymongo import MongoClient
from random import randint
#
from components.fetch import fetch_db_url

def connect() -> MongoClient:
  client = MongoClient(fetch_db_url())
  db = client.diana_wisdom
  collection = db.quotes

  return collection

def get_random_quote() -> dict:
  collection = connect()
  _max = collection.count_documents({})
  _random = randint(1, _max)
  quote = collection.find_one({ 'id': _random })

  return quote

def get_docs_count() -> int:
  collection = connect()
  _max = collection.count_documents({})

  return _max
