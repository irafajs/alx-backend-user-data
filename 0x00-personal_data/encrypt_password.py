#!/usr/bin/env python3
"""
Shebang to create a PY script
"""


import bcrypt


def hash_password(password: str) -> bytes:
    """method to encrypt password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Method to check if encrypted password is valid"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
