import pymongo
import datetime

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)
db = client["UserScript"]
collection = db["user_script"]


script = {
    "owner": 1,
    "language": "python3",
    "program": [{"filename": "test.py", "content": "print(Hello, World!)"}],
    "created_at": datetime.datetime.now(),
    "updated_at": datetime.datetime.now()
}

#x = collection.insert_one(script)


x = collection.find_one({"_id": ObjectId("5fce357a20ef468d5ee847bd")})
print(x)
