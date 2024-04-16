#!/usr/bin/env python3
"""
Shebang to create a PY script
"""


import base64
from api.v1.auth.auth import Auth


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
