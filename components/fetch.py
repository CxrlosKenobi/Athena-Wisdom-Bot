import json

def fetch_token():
  with open("config.json", "r") as file:
    get = json.load(file)
  return get["token"]

def fetch_db_url():
  with open("config.json", "r") as file:
    get = json.load(file)
  return get["db_url"]

