#!/usr/bin/env python3
"""
Shebang to create a PY script
"""


from flask import request
from typing import List, TypeVar


class Auth:
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
