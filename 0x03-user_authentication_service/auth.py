#!/usr/bin/env python3
"""
Shebang to create a PY script
"""


import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """method to hash the password"""
    salt = bcrypt.gensalt()
    hash_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_pass


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """method to save the user with hashed password if he doesn't exist"""
        try:
            find_user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists.')
        except NoResultFound:
            pass
        hash_pass = _hash_password(password)
        save_user = self._db.add_user(email=email, hashed_password=hash_pass)
        return save_user
