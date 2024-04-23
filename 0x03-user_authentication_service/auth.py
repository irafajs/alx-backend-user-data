#!/usr/bin/env python3
"""
Shebang to create a PY script
"""


import bcrypt


def _hash_password(password: str) -> bytes:
    """method to hash the password"""
    salt = bcrypt.gensalt()
    hash_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_pass
