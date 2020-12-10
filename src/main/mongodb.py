import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from .jwt import verify


def create_userscript_database_file(owner, language, files, main_file):
    script = {
        "owner": owner,
        "language": language,
        "program": files,
        "main_file": main_file,
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now()
    }
    return script


class MongoDbActions:
    def __init__(self, database):
        client = MongoClient('localhost', 27017)
        db = client["UserScript"]
        self.collection = db[database]

    def create_userscript(self, jwt, files, main_file, language):
        info = verify(jwt)
        if info is None:
            return None

        script = create_userscript_database_file(info["sub"], language, files, main_file)
        insertion = self.collection.insert_one(script)
        return insertion.inserted_id

    def update_userscript(self, jwt, object_id, language=None, files=None, main_file=None):
        info = verify(jwt)
        if info is None:
            return None

        user = info["sub"]
        role = info["role"]
        owner = self.find_userscript(object_id)["owner"]
        if owner == user or role == "admin":
            script = {}
            if language is not None:
                script["language"] = language
            if files is not None:
                script["program"] = files
            if main_file is not None:
                script["main_file"] = main_file
            script["updated_at"] = datetime.datetime.now()
            update = { "$set": script}
            return self.collection.update_one({"_id": ObjectId(object_id)}, update)
        return None

    def find_userscript(self, object_id):
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def delete_userscript(self, jwt, object_id):
        info = verify(jwt)
        if info is None:
            return None

        user = info["sub"]
        role = info["role"]
        owner = self.find_userscript(object_id)
        if owner is not None:
            owner = owner["owner"]
            if owner == user or role == "admin":
                return self.collection.delete_one({'_id': ObjectId(object_id)})
        return None
