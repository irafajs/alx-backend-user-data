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
        if path is None:
            return True
        elif excluded_paths is None or len(excluded_paths) == 0:
            return True
        else:
            for excluded_path in excluded_paths:
                if path.startswith(excluded_path.rstrip('/')):
                    return False
            return True

    def authorization_header(self, request=None) -> str:
        """method to handle flask request object"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """method to handle current user"""
        return None
