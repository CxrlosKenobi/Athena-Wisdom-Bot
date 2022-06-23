import json

def fetch_token() -> str:
  with open("config.json", "r") as file:
    get = json.load(file)
  return get["token"]

def fetch_db_url() -> str:
  with open("config.json", "r") as file:
    get = json.load(file)
  return get["db_url"]

