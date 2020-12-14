from unittest import TestCase
from ..main.jwt import verify


class Test(TestCase):
    def test_verify_working_token(self):
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1Iiwicm9sZSI6InVzZXIiLCJpc3MiOiJJbWFnZUhvc3Quc2R1LmRrIiwiZXhwIjoxNjM4NTYwNzEzLCJpYXQiOjE2MDcwMjQ3MTN9._AErjVtL5cs72HNi55LMhDi2VLhH-VDKr09_7gBGwDg"
        actual = verify(token)
        expected = {'sub': '5', 'role': 'user', 'iss': 'ImageHost.sdu.dk', 'exp': 1638560713, 'iat': 1607024713}
        self.assertEqual(expected, actual)

    def test_verify_expired_token(self):
        expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIiwicm9sZSI6ImFkbWluIiwiaXNzIjoiSW1hZ2VIb3N0LnNkdS5kayIsImV4cCI6MTYwNjkyODMwMywiaWF0IjoxNjA2OTI0NzAzfQ.TC5wpxA20V-zhorK0EVIQbjIZdPX2Uy-PLrw7mYIeng"
        actual = verify(expired_token)
        expected = None
        self.assertEqual(expected, actual)
