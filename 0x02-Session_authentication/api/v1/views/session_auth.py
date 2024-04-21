#!/usr/bin/env python3
"""
Shebang to create a py script
"""


from flask import jsonify, request
from api.v1.views import app_views
from os import getenv


SESSION_NAME = getenv("SESSION_NAME", "_my_session_id")


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
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
    session_id = auth.create_session(user[0].id)
    response = jsonify(user[0].to_json())
    response.set_cookie(SESSION_NAME, session_id)
    return response
