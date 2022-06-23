import json

def fetch_config(request):
  with open("config.json", "r") as file:
    get = json.load(file)
  data = request['key']

  return get[data]
