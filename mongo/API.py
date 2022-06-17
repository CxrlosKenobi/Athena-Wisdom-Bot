from  pymongo import MongoClient

client = MongoClient("mongodb+srv://kenobi:6235539a@sandbox.hdyam.mongodb.net/admin")
db = client.diana_wisdom
collection = db.quotes