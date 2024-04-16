#!/usr/bin/env python3
"""
Shebang to create a PY script
"""


from flask import request
from typing import List, TypeVar


class Auth:
    """class to manage APU authentications"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method require_auth"""
        return False

    def authorization_header(self, request=None) -> str:
        """method to handle flask request object"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """method to handle current user"""
        return None
