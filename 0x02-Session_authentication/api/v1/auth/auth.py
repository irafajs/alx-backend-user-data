#!/usr/bin/env python3
"""
Shebang to create a PY script
"""


from flask import request
import os
from os import getenv
from typing import List, TypeVar


class Auth:
    """class auth to authenticate user"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Public method to require authentication"""
        if path is None:
            return True
        elif excluded_paths is None or len(excluded_paths) == 0:
            return True
        else:
            for excluded_path in excluded_paths:
                if excluded_path.endswith('*'):
                    if path.startswith(excluded_path[:-1]):
                        return False
                elif path == excluded_path or path + '/' == excluded_path:
                    return False
            return True

    def authorization_header(self, request=None) -> str:
        """method to handle flask request object"""
        if request is None:
            return None
        elif 'Authorization' not in request.headers:
            return None
        else:
            return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """method to handle current user"""
        return None

    def session_cookie(self, request=None):
        """method that returns a cooke value from a request"""
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
