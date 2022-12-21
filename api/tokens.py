from time import time

from cryptography.hazmat.backends import \
    default_backend as crypto_default_backend
from cryptography.hazmat.primitives import \
    serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from faker import Faker
from jwt import decode, encode

from orm import Users
from token_secrets import PRIVATE_KEY, PUBLIC_KEY

faker = Faker()


def generate_key_pairs():
    key = rsa.generate_private_key(
        backend=crypto_default_backend(), public_exponent=65537, key_size=2048
    )

    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption(),
    )

    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH, crypto_serialization.PublicFormat.OpenSSH
    )
    return private_key, public_key


def create_token(user_data: Users) -> str:
    claims = {
        "id": user_data.id,
        "email": user_data.email,
        "name": user_data.name,
        "description": user_data.description,
        "user_status": user_data.user_status,
        "role": user_data.role,
        "exp": int(time() + 120000),
        "iat": int(time()),
        "version": faker.pyint(),
        "jti": faker.uuid4(),
        "client_id": faker.uuid4(),
    }
    return encode(claims, PRIVATE_KEY, algorithm="RS256")


def validate_token(token):
    return decode(token, PUBLIC_KEY, algorithms=["RS256"])
