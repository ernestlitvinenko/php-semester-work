import asyncio
import typing

import bcrypt
from mongoengine import Document, StringField, EmailField, BooleanField, ListField
from mongoengine.errors import NotUniqueError
from models.mongo_models.base_model import ToDictMixin


class UserExistsException(Exception):
    def __init__(self, identifier: str, *args):
        self.identifier = identifier

    def __str__(self):
        return f"User with {self.identifier} is already exists"


class User(Document, ToDictMixin):
    username = StringField(required=True)
    email = EmailField(required=False)
    password = StringField(required=True)
    is_admin = BooleanField(default=False)
    items = ListField(default=[])

    @staticmethod
    def generate_password(clean_pwd: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(clean_pwd.encode('utf-8'), salt).decode('utf-8')

    def check_pwd(self, clean_pwd: str) -> bool:
        return bcrypt.checkpw(clean_pwd.encode('utf-8'), self.password.encode('utf-8'))

    @classmethod
    async def create_user(cls, username: str, email: str | None, password: str) -> typing.Optional['User']:
        loop = asyncio.get_running_loop()
        hashed_pwd = await loop.run_in_executor(None, cls.generate_password, password)
        try:
            return cls(username=username, email=email, password=hashed_pwd).save()
        except NotUniqueError:
            raise UserExistsException(f'username="{username}" or email="{email}"')

    meta = {
        'indexes': [
            {
                "fields": ['username'],
                "unique": True
            },
            {
                "fields": ['email'],
                "unique": True
            }
        ]
    }
