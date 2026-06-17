from pymongo import MongoClient

client = MongoClient(
    "mongodb://localhost:27017/"
)

db = client["twin_ai"]

appearance_collection = db["appearance"]