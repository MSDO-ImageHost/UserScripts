import datetime
import os
import threading
from pymongo import MongoClient
from bson.objectid import ObjectId
from jwt import verify
from JobLauncher import Job

try:
    USERNAME = os.environ["MONGO_USERNAME"]
    PASSWORD = os.environ["MONGO_PASSWORD"]
    HOST = os.environ["MONGO_HOST"]
except KeyError:
    USERNAME = ""
    PASSWORD = ""
    HOST = "localhost"


def create_userscript_database_file(owner, language, files, main_file):
    script = {
        "owner": owner,
        "language": language,
        "program": files,
        "main_file": main_file,
        "logs": [],
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now()
    }
    return script


class MongoDbActions:
    def __init__(self, collection_userscripts):
        client = MongoClient(HOST, username=USERNAME, password=PASSWORD)
        db = client["UserScript"]
        self.collection = db[collection_userscripts]

    def __permitted_action(self, jwt, object_id):
        info = verify(jwt)
        if info is None:
            return "Invalid jwt"
        user = info["sub"]
        role = info["role"]
        files = self.find_userscript(object_id)
        if files is not None:
            owner = files["owner"]
            if str(owner) == str(user) or role > 9:
                return files
            return "Permission denied"
        return "File does not exist"

    def find_userscript(self, object_id):
        return self.collection.find_one({"_id": ObjectId(object_id)})

    def find_users_userscripts(self, jwt, user):
        # Authenticate
        info = verify(jwt)
        if info is None:
            return "Invalid jwt"
        if str(info["sub"]) == str(user) or info["role"] > 9:
            # find all user's userscripts
            return [userscript for userscript in self.collection.find({"owner": user})]
        return "Permission denied"

    def create_userscript(self, jwt, files, main_file, language):
        # Authenticate
        info = verify(jwt)
        if info is None:
            return "Invalid jwt"
        # setup structure of userscript
        script = create_userscript_database_file(info["sub"], language, files, main_file)
        # create userscript in database
        insertion = self.collection.insert_one(script)
        return insertion.inserted_id

    def update_userscript(self, jwt, object_id, updated_language=None, updated_files=None, updated_main_file=None):
        # Authenticate and read userscript from database
        files = self.__permitted_action(jwt, object_id)
        if isinstance(files, str):
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
        if isinstance(files, str):
            return files
        # Delete userscript from database
        return self.collection.delete_one({'_id': ObjectId(object_id)})

    def run_userscript(self, jwt, object_id):
        # Authenticate and read userscript from database
        files = self.__permitted_action(jwt, object_id)
        if isinstance(files, str):
            return files

        # Run userscript
        job = Job(object_id)

        new_thread = threading.Thread(target=job.job_starter, args=(files["language"], files["program"], files["main_file"]))
        new_thread.start()

    def create_log(self, log, program_id):
        log_object = {
            "log": log,
            "created_at": datetime.datetime.now()
        }
        return self.collection.update({'_id': ObjectId(program_id)}, {'$push': {'logs': log_object}})["nModified"]

