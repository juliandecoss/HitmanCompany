from hashlib import sha256
from hmac import new


def encrypt(password: str) -> str:
    return new(key="".encode(), msg=password.encode(), digestmod=sha256).hexdigest()


def check_password(password, realpassword) -> bool:
    attempt_password = encrypt(password)
    return realpassword == attempt_password
