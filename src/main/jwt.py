from jose import jwt
from jose import exceptions


# It decodes the token and makes sure that the issuer is what we expect and that it has not expired
def verify(jwt_token):
    try:
        decoded = jwt.decode(jwt_token, "secret", algorithms=['HS256'])
        if decoded["iss"] == "ImageHost.sdu.dk":
            return decoded
    except exceptions.ExpiredSignatureError:
        return None
