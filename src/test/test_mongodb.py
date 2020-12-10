from unittest import TestCase
from ..main.mongodb import *


class Test(TestCase):
    def test_create_userscript_database_file(self):
        owner = 5
        language = "python"
        with open("src/test/test_scripts/test.py", "rb") as file:
            file_content = file.read()
        file = {"filename": "hello.py", "content": file_content}
        main_file = "hello.py"
        actual = create_userscript_database_file(owner, language, [file], main_file)
        expected = {
            "owner": 5,
            "language": "python",
            "program": [{"filename": "hello.py", "content": file_content}],
            "main_file": "hello.py",
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now()
        }
        self.assertEqual(expected, actual)


class TestMongoDbActions(TestCase):
    def setUp(self):
        self.mg = MongoDbActions("Testing")

    def tearDown(self):
        self.mg.collection.drop()

    def test_create_userscript_and_find_userscript(self):
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"
        with open("src/test/test_scripts/test.py", "rb") as file:
            file_content = file.read()
        file = {"filename": "hello.py", "content": file_content}
        main_file = "hello.py"
        language = "python"
        userscript_id = self.mg.create_userscript([file], main_file, language, jwt_token)
        userscript_found = self.mg.find_userscript(userscript_id)
        self.assertEqual(userscript_id, userscript_found["_id"])

    def test_create_userscript_with_outdated_token(self):
        expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIiwicm9sZSI6ImFkbWluIiwiaXNzIjoiSW1hZ2VIb3N0LnNkdS5kayIsImV4cCI6MTYwNjkyODMwMywiaWF0IjoxNjA2OTI0NzAzfQ.TC5wpxA20V-zhorK0EVIQbjIZdPX2Uy-PLrw7mYIeng"
        with open("src/test/test_scripts/test.py", "rb") as file:
            file_content = file.read()
        file = {"filename": "hello.py", "content": file_content}
        main_file = "hello.py"
        language = "python"
        actual = self.mg.create_userscript([file], main_file, language, expired_token)
        expected = None
        self.assertEqual(expected, actual)

    def test_find_userscript_non_existing(self):
        id_doesnt_exist = "5fd229c6928aa1351adbd4ee"
        userscript_found = self.mg.find_userscript(id_doesnt_exist)
        self.assertEqual(userscript_found, None)

    def test_create_userscript_and_delete_userscript(self):
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"
        with open("src/test/test_scripts/test.py", "rb") as file:
            file_content = file.read()
        file = {"filename": "hello.py", "content": file_content}
        main_file = "hello.py"
        language = "python"
        userscript_id = self.mg.create_userscript([file], main_file, language, jwt_token)
        userscript_deleted = self.mg.delete_userscript(userscript_id)
        self.assertEqual(userscript_deleted.deleted_count, 1)

    def test_delete_userscript_non_existing(self):
        id_doesnt_exist = "5fd229c6928aa1351adbd4ee"
        userscript_deleted = self.mg.delete_userscript(id_doesnt_exist)
        self.assertEqual(userscript_deleted.deleted_count, 0)

    def test_update_userscript(self):
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"
        with open("src/test/test_scripts/test.py", "rb") as file:
            file_content = file.read()
        file = {"filename": "hello.py", "content": file_content}
        main_file = "hello.py"
        language = "python"
        userscript_id = self.mg.create_userscript([file], main_file, language, jwt_token)

        updated_script = self.mg.update_userscript(userscript_id, "java", [file], main_file)
        self.assertEqual(1, updated_script.modified_count)
