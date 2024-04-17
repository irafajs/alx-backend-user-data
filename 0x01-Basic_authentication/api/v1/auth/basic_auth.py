#!/usr/bin/env python3
"""
Shebang to create a PY script
"""


import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """class basic auth"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """handle base64 of authorization"""
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        elif not authorization_header.startswith('Basic '):
            return None
        else:
            auth_type = authorization_header.split()
            return auth_type[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """method to decode the header"""
        if base64_authorization_header is None:
            return None
        if not isinstance(
                base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except Exception as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """extract username and password"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        colon_exist = decoded_base64_authorization_header.find(':')
        if colon_exist == -1:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """handle user instance based on credentials"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        User.load_from_file()
        users = User.search({'email': user_email})
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """method to overide auth"""
        if request is None:
            return None
        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None
        base64_header = self.extract_base64_authorization_header(
                authorization_header)
        if base64_header is None:
            return None
        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None
        user_credentials = self.extract_user_credentials(decoded_header)
        if user_credentials is None:
            return None
        user_email, user_pwd = user_credentials
        return self.user_object_from_credentials(user_email, user_pwd)
