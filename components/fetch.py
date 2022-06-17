import json

def fetch_token():
  with open("config.json", "r") as file:
    get = json.load(file)
  return get["token"]

