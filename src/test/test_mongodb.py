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

    def create_userscript_default(self, jwt_token):
        with open("src/test/test_scripts/test.py", "rb") as file:
            file_content = file.read()
        file = {"filename": "hello.py", "content": file_content}
        main_file = "hello.py"
        language = "python"
        return self.mg.create_userscript(jwt_token, [file], main_file, language)

    def test_create_userscript_and_find_userscript(self):
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"
        userscript_id = self.create_userscript_default(jwt_token)
        userscript_found = self.mg.find_userscript(userscript_id)
        self.assertEqual(userscript_id, userscript_found["_id"])

    def test_create_userscript_with_outdated_token(self):
        expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIiwicm9sZSI6ImFkbWluIiwiaXNzIjoiSW1hZ2VIb3N0LnNkdS5kayIsImV4cCI6MTYwNjkyODMwMywiaWF0IjoxNjA2OTI0NzAzfQ.TC5wpxA20V-zhorK0EVIQbjIZdPX2Uy-PLrw7mYIeng"
        actual = self.create_userscript_default(expired_token)
        expected = None
        self.assertEqual(expected, actual)

    def test_find_userscript_non_existing(self):
        id_doesnt_exist = "5fd229c6928aa1351adbd4ee"
        actual = self.mg.find_userscript(id_doesnt_exist)
        expected = None
        self.assertEqual(expected, actual)

    def test_create_userscript_and_delete_userscript(self):
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"
        userscript_id = self.create_userscript_default(jwt_token)
        userscript_deleted = self.mg.delete_userscript(jwt_token, userscript_id)
        actual = userscript_deleted.deleted_count
        expected = 1
        self.assertEqual(expected, actual)

    def test_delete_userscript_with_bad_deletor(self):
        jwt_token_creator = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"
        jwt_token_deletor = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjU0MDMyMDAsImlhdCI6MTY2NTQwMzIwMCwiaXNzIjoiSW1hZ2VIb3N0LnNkdS5kayIsInJvbGUiOjAsInN1YiI6IjEyIn0.0KKTtjDmMjQ9uRryM5LGGYK5Ko_sDsuCH_PqSIPrD2I"
        userscript_id = self.create_userscript_default(jwt_token_creator)
        actual = self.mg.delete_userscript(jwt_token_deletor, userscript_id)
        expected = None
        self.assertEqual(expected, actual)

    def test_delete_userscript_non_existing(self):
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"
        id_doesnt_exist = "5fd229c6928aa1351adbd4ee"
        actual = self.mg.delete_userscript(jwt_token, id_doesnt_exist)
        expected = None
        self.assertEqual(expected, actual)

    def test_update_userscript(self):
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"
        userscript_id = self.create_userscript_default(jwt_token)
        updated_script = self.mg.update_userscript(jwt_token, userscript_id, "java")
        actual = updated_script.modified_count
        expected = 1
        self.assertEqual(expected, actual)

    def test_update_userscript_with_bad_updator(self):
        jwt_token_creator = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"
        jwt_token_updator = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjU0MDMyMDAsImlhdCI6MTY2NTQwMzIwMCwiaXNzIjoiSW1hZ2VIb3N0LnNkdS5kayIsInJvbGUiOjAsInN1YiI6IjEyIn0.0KKTtjDmMjQ9uRryM5LGGYK5Ko_sDsuCH_PqSIPrD2I"
        userscript_id = self.create_userscript_default(jwt_token_creator)
        actual = self.mg.update_userscript(jwt_token_updator, userscript_id, "java")
        expected = None
        self.assertEqual(expected, actual)

    def test_update_userscript_non_existing(self):
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"
        id_doesnt_exist = "5fd229c6928aa1351adbd4ee"
        actual = self.mg.update_userscript(jwt_token, id_doesnt_exist, "java")
        expected = None
        self.assertEqual(expected, actual)
