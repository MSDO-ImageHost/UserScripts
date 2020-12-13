from unittest import TestCase
from ..main.rabbitmq import *


class Test(TestCase):
    def test_send_CreateUserScript(self):
        event = "CreateUserScript"
        with open("src/test/test_scripts/wait.py", "r") as file:
            file_content = file.read()
        with open("src/test/test_scripts/requirements.txt", "r") as file:
            req = file.read()
        data = {
            "program": [{"filename": "wait.py", "content": file_content}, {"filename": "requirements.txt", "content": req}],
            "main_file": "wait.py",
            "language": "python"
        }
        status_code = 200
        message = "Hi"
        correlation_id = "42"
        content_type = "application/json"
        jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"

        send(event, data, status_code, message, correlation_id, content_type, jwt)

    def test_send_RunUserScript(self):
        event = "RunUserScript"
        data = {
            "user_script": "5fd60d376a4d9affdb1ed8c3"
        }
        status_code = 200
        message = "Hi"
        correlation_id = "42"
        content_type = "application/json"
        jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"

        send(event, data, status_code, message, correlation_id, content_type, jwt)

    def test_send_DeleteUserScript(self):
        event = "DeleteUserScript"
        data = {
            "user_script": "5fd5d354685a4a28c3d61c39"
        }
        status_code = 200
        message = "Hi"
        correlation_id = "42"
        content_type = "application/json"
        jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"

        send(event, data, status_code, message, correlation_id, content_type, jwt)
