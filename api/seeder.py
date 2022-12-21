from faker import Faker

from encrypt import encrypt
from transactions import create_user

faker = Faker()

psswd = encrypt("password")
dict = {
    "email": "giussepemarota@gmail.com",
    "name": "Giussepe Meatza",
    "password": encrypt("password"),
    "description": "You are fired bastard",
}
create_user(dict)
for manager in range(3):
    dict = {
        "email": faker.email(),
        "name": faker.name(),
        "password": psswd,
        "description": "I am manager ready to ask what else guys",
        "role": "Manager",
    }
    create_user(dict)

for manager in range(9):
    dict = {
        "email": faker.email(),
        "name": faker.name(),
        "password": psswd,
        "description": "I am a hitman ready to be killed",
    }
    create_user(dict)
