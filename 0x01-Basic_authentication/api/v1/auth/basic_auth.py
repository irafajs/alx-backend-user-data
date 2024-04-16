#!/usr/bin/env python3
"""
Shebang to create a PY script
"""


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
