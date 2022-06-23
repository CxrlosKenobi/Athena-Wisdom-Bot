import json

def hist_handler(_id: int) -> bool:
  with open("mongo/history.json", "r") as file:
    hist = json.load(file)

  updated = {}
  if _id not in hist.values():
    for key, value in hist.items():
      if int(key) == len(hist):
        updated[key] = _id
      else:
        updated[key] = hist[str(int(key) + 1)]

    with open("mongo/history.json", "w") as file:
      json.dump(updated, file, indent=2)
    
    return True
  else:
    return False

