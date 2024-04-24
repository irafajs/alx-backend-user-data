#!/usr/bin/env python3
"""
Shebang to create a PY script
"""


import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
import uuid


def _hash_password(password: str) -> bytes:
    """method to hash the password"""
    salt = bcrypt.gensalt()
    hash_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_pass


def _generate_uuid() -> str:
    """method to generate uuid"""
    gen_uuid = str(uuid.uuid4())
    return gen_uuid


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

    def valid_login(self, email: str, password: str) -> bool:
        """method to validate a loging in of a user"""
        try:
            find_user = self._db.find_user_by(email=email)
            if find_user:
                hashed_pass = find_user.hashed_password
                check_pass = bcrypt.checkpw(
                        password.encode('utf-8'), hashed_pass)
                return check_pass
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """method to generate a session id"""
        try:
            find_user = self._db.find_user_by(email=email)
            if find_user:
                user_id = find_user.id
                session_id = _generate_uuid()
                self._db.update_user(user_id=user_id, session_id=session_id)
                return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """method to return user using generated session_id or none"""
        try:
            find_user = self._db.find_user_by(session_id=session_id)
            return find_user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """method to destroy a given session by user_id"""
        try:
            find_user = self._db.find_user_by(user_id=user_id)
            self._db.update_user(user_id=user_id, session_id=None)
            return None
        except NoResultFound:
            return None
