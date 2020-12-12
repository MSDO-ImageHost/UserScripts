import datetime
import os
import shutil

from pymongo import MongoClient
from bson.objectid import ObjectId
from .jwt import verify
from ..main.ContainerLauncher import Container


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

    def __permitted_action(self, jwt, object_id):
        info = verify(jwt)
        if info is None:
            return None
        user = info["sub"]
        role = info["role"]
        files = self.find_userscript(object_id)
        if files is not None:
            owner = files["owner"]
            if owner == user or role == "admin":
                return files
        return None

    def find_userscript(self, object_id):
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def find_users_userscripts(self, jwt, user):
        # Authenticate
        info = verify(jwt)
        if info is None:
            return None
        if info["sub"] == user or info["role"] == "admin":
            # find all user's userscripts
            return self.collection.find({"owner": user})
        return None

    def create_userscript(self, jwt, files, main_file, language):
        # Authenticate
        info = verify(jwt)
        if info is None:
            return None
        # setup structure of userscript
        script = create_userscript_database_file(info["sub"], language, files, main_file)
        # create userscript in database
        insertion = self.collection.insert_one(script)
        return insertion.inserted_id

    def update_userscript(self, jwt, object_id, updated_language=None, updated_files=None, updated_main_file=None):
        # Authenticate and read userscript from database
        files = self.__permitted_action(jwt, object_id)
        if files is None:
            return files
        # setup changes for userscript
        script = {}
        if updated_language is not None:
            script["language"] = updated_language
        if updated_files is not None:
            script["program"] = updated_files
        if updated_main_file is not None:
            script["main_file"] = updated_main_file
        script["updated_at"] = datetime.datetime.now()
        update = {"$set": script}
        # Update userscript
        return self.collection.update_one({"_id": ObjectId(object_id)}, update)

    def delete_userscript(self, jwt, object_id):
        # Authenticate and read userscript from database
        files = self.__permitted_action(jwt, object_id)
        if files is None:
            return files
        # Delete userscript from database
        return self.collection.delete_one({'_id': ObjectId(object_id)})

    def run_userscript(self, jwt, object_id):
        # Authenticate and read userscript from database
        files = self.__permitted_action(jwt, object_id)
        if files is None:
            return files
        # create program files
        path = "user_scripts/" + object_id + "/"
        os.mkdir(path)
        for file in files["program"]:
            with open(path + file["filename"], "x") as f:
                f.write(file["content"].decode("utf-8"))
        # Run userscript
        root_dir = os.path.dirname(os.path.abspath("README.md"))
        volume_path = root_dir + "/user_scripts/" + object_id
        c = Container(volume_path)
        output = c.container_starter(files["language"], files["main_file"])
        # Delete program files
        shutil.rmtree(volume_path)
        return output
