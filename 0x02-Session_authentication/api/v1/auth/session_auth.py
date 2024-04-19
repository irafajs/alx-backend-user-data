#!/usr/bin/env python3
"""
Shebang to create a PY script
"""

from flask import jsonify, request
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from os import getenv
import uuid

SESSION_NAME = getenv("SESSION_NAME", "_my_session_id")


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


@app_views.route(
        '/auth_session/login/', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """method to handle login and the sessions"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    from models.user import User
    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    auth = SessionAuth()
    session_id = auth.create_session(user[0].id)
    response = jsonify(user[0].to_json())
    response.set_cookie(SESSION_NAME, session_id)
    return response
