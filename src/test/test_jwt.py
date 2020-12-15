from unittest import TestCase
from ..main.jwt import verify


class Test(TestCase):
    def test_verify_working_token(self):
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIiwicm9sZSI6MSwiaXNzIjoiSW1hZ2VIb3N0LnNkdS5kayIsImV4cCI6MTYwODUyMDMyOSwiaWF0IjoxNjA3MjA2MzI5fQ.EFv8rHJYAp0DE8h2GFzZzceCiOZS4ZfCh6aBkIHNsEs"
        actual = verify(token)
        expected = {'exp': 1608520329, 'iat': 1607206329, 'iss': 'ImageHost.sdu.dk', 'role': 1, 'sub': '1'}
        self.assertEqual(expected, actual)

    def test_verify_expired_token(self):
        expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIiwicm9sZSI6ImFkbWluIiwiaXNzIjoiSW1hZ2VIb3N0LnNkdS5kayIsImV4cCI6MTYwNjkyODMwMywiaWF0IjoxNjA2OTI0NzAzfQ.TC5wpxA20V-zhorK0EVIQbjIZdPX2Uy-PLrw7mYIeng"
        actual = verify(expired_token)
        expected = None
        self.assertEqual(expected, actual)
