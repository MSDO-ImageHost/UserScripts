import pymongo
import datetime

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)
db = client["UserScript"]
collection = db["user_script"]


script = {
    "owner": 2,
    "language": "python3",
    "program": [{"filename": "test.py", "content": "print(Hello, World!)"}],
    "created_at": datetime.datetime.now(),
    "updated_at": datetime.datetime.now()
}

updated_script = {
    "$set": {
        "owner": 2,
        "language": "python3",
        "program": [{"filename": "test.py", "content": "print(Hello, World!)"}],
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now()
    }
}

#x = collection.insert_one(script)


def update_userscript(object_id, userscript):
    return collection.update_one(object_id, userscript)


def find_userscript(object_id):
    return collection.find_one({"_id": ObjectId(object_id)})


def delete_userscript(object_id):
    return collection.delete_one({'_id': ObjectId(object_id)})


#print(find_userscript("5fcecf774ba4c7a206723075"))
print(update_userscript("5fcecf774ba4c7a206723075", updated_script))

