from  pymongo import MongoClient

client = MongoClient("mongodb+srv://kenobi:6235539a@sandbox.hdyam.mongodb.net/admin")

db = client.sample_guides
collection = db.planets

# Print the first 5 documents in the collection
for planet in collection.find().limit(5):
    print(planet)
