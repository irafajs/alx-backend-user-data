#!/usr/bin/env python3
"""
Shebang to create a PY script
"""

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """class sessionauth to create a session mechanism"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """methdo to create a session ID for the user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """method to return user besed on session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """method to return a user instance based on cookie value"""
        from models.user import User
        session_id = self.session_cookie(request)
        if session_id:
            user_id = self.user_id_for_session_id(session_id)
            if user_id:
                return User.get(user_id)
        return None
