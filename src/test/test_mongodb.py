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
            'logs': [],
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
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIiwicm9sZSI6MSwiaXNzIjoiSW1hZ2VIb3N0LnNkdS5kayIsImV4cCI6MTYwODUyMDMyOSwiaWF0IjoxNjA3MjA2MzI5fQ.EFv8rHJYAp0DE8h2GFzZzceCiOZS4ZfCh6aBkIHNsEs"
        userscript_id = self.create_userscript_default(jwt_token)
        userscript_found = self.mg.find_userscript(userscript_id)
        self.assertEqual(userscript_id, userscript_found["_id"])

    def test_create_userscript_with_outdated_token(self):
        expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIiwicm9sZSI6ImFkbWluIiwiaXNzIjoiSW1hZ2VIb3N0LnNkdS5kayIsImV4cCI6MTYwNjkyODMwMywiaWF0IjoxNjA2OTI0NzAzfQ.TC5wpxA20V-zhorK0EVIQbjIZdPX2Uy-PLrw7mYIeng"
        actual = self.create_userscript_default(expired_token)
        expected = "Invalid jwt"
        self.assertEqual(expected, actual)

    def test_find_userscript_non_existing(self):
        id_doesnt_exist = "5fd229c6928aa1351adbd4ee"
        actual = self.mg.find_userscript(id_doesnt_exist)
        expected = None
        self.assertEqual(expected, actual)

    def test_create_userscript_and_delete_userscript(self):
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIiwicm9sZSI6MSwiaXNzIjoiSW1hZ2VIb3N0LnNkdS5kayIsImV4cCI6MTYwODUyMDMyOSwiaWF0IjoxNjA3MjA2MzI5fQ.EFv8rHJYAp0DE8h2GFzZzceCiOZS4ZfCh6aBkIHNsEs"
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
        expected = "Permission denied"
        self.assertEqual(expected, actual)

    def test_delete_userscript_non_existing(self):
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"
        id_doesnt_exist = "5fd229c6928aa1351adbd4ee"
        actual = self.mg.delete_userscript(jwt_token, id_doesnt_exist)
        expected = "File does not exist"
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
        expected = "Permission denied"
        self.assertEqual(expected, actual)

    def test_update_userscript_non_existing(self):
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"
        id_doesnt_exist = "5fd229c6928aa1351adbd4ee"
        actual = self.mg.update_userscript(jwt_token, id_doesnt_exist, "java")
        expected = "File does not exist"
        self.assertEqual(expected, actual)

    def test_find_users_userscripts(self):
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"
        user = "5"
        self.create_userscript_default(jwt_token)
        self.create_userscript_default(jwt_token)
        output = self.mg.find_users_userscripts(jwt_token, user)
        actual = 0
        for _ in output:
            actual += 1
        expected = 2
        self.assertEqual(expected, actual)

    def test_find_users_userscripts_not_allowed_user(self):
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6MCwiaXNzIjoiSW1hZ2VIb3N0LnNkdS5kayIsImV4cCI6MTYzODU2MDcxMywiaWF0IjoxNjA3MDI0NzEzfQ.BEd5MV1_8Vukwk-zX3cNKrXKF_ZseIBmahYt7-PopB8"
        user = "3"
        self.create_userscript_default(jwt_token)
        self.create_userscript_default(jwt_token)
        actual = self.mg.find_users_userscripts(jwt_token, user)
        expected = "Permission denied"
        self.assertEqual(expected, actual)

    def test_run_userscript(self):
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6MCwiaXNzIjoiSW1hZ2VIb3N0LnNkdS5kayIsImV4cCI6MTYzODU2MDcxMywiaWF0IjoxNjA3MDI0NzEzfQ.BEd5MV1_8Vukwk-zX3cNKrXKF_ZseIBmahYt7-PopB8"
        userscript_id = self.create_userscript_default(jwt_token)
        actual = self.mg.run_userscript(jwt_token, str(userscript_id))
        expected = None
        self.assertEqual(expected, actual)

    def test_run_userscript_non_existing(self):
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"
        userscript_id = "5fd229c6928aa1351adbd4ee"
        actual = self.mg.run_userscript(jwt_token, str(userscript_id))
        expected = "File does not exist"
        self.assertEqual(expected, actual)

    def test_run_userscript_not_allowed_user(self):
        jwt_token_creator = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"
        jwt_token_runner = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjU0MDMyMDAsImlhdCI6MTY2NTQwMzIwMCwiaXNzIjoiSW1hZ2VIb3N0LnNkdS5kayIsInJvbGUiOjAsInN1YiI6IjEyIn0.0KKTtjDmMjQ9uRryM5LGGYK5Ko_sDsuCH_PqSIPrD2I"
        userscript_id = self.create_userscript_default(jwt_token_creator)
        actual = self.mg.run_userscript(jwt_token_runner, str(userscript_id))
        expected = "Permission denied"
        self.assertEqual(expected, actual)

    def test_create_log(self):
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"
        userscript_id = self.create_userscript_default(jwt_token)
        log = "hi there!\n this works right?"
        actual = self.mg.create_log(log, userscript_id)
        expected = 1
        self.assertEqual(expected, actual)

    def test_create_log_fail(self):
        userscript_id = "5cd604ce45c4812e05c24f2c"
        log = "hi there!\n this works right?"
        actual = self.mg.create_log(log, userscript_id)
        expected = 0
        self.assertEqual(expected, actual)
