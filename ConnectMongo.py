from pymongo import MongoClient
from pymongo.collection import Collection
from Configurations import Config

MONGODB_URI = Config.mongodb_uri()
# print(f"Connecting to MongoDB at {MONGODB_URI}")
print(f"Connecting to MongoDB.....")
mongo_client = MongoClient(MONGODB_URI)
mongo_db = mongo_client[Config.MONGODB_DBNAME]
collection: Collection = mongo_db[Config.MONGODB_COLLECTION]
print("Connected to MongoDB")
