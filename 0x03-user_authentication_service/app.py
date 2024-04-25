#!/usr/bin/env python3
"""
Shebang to create a py script
"""


from auth import Auth
from flask import Flask, jsonify, request, abort, make_response
from flask import redirect
from sqlalchemy.orm.exc import NoResultFound

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def home() -> str:
    """method to handle homepage"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_users() -> str:
    """method to register a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email=email, password=password)
        return {"email": email, "message": "user created"}, 200
    except ValueError:
        return {"message": "email already registered"}, 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """method to handle user login"""
    email = request.form.get('email')
    password = request.form.get('password')
    check_valid = AUTH.valid_login(email=email, password=password)
    if check_valid:
        session_id = AUTH.create_session(email=email)
        response = make_response({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """method to logout the user"""
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    get_user = AUTH.get_user_from_session_id(session_id)
    if get_user is None:
        abort(403)
    AUTH.destroy_session(get_user.id)
    return redirect("/")


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """method to load the user profile"""
    try:
        session_id = request.cookies.get('session_id')
        if not session_id:
            abort(403)
        get_user = AUTH.get_user_from_session_id(session_id)
        if get_user:
            return {"email": get_user.email}, 200
        else:
            abort(403)
    except NoResultFound:
        abort(403)


@app.route('/reset_password', methods=['POST', 'PUT'], strict_slashes=False)
def get_reset_password_token() -> str:
    """method to handle password reset by token"""
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            reset_token = AUTH.get_reset_password_token(email)
            return {"email": email, "reset_token": reset_token}, 200
        except ValueError:
            abort(403)
    if request.method == 'PUT':
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        password = request.form.get('password')
        try:
            get_user = AUTH.get_user_from_session_id(email=email)
            if get_user.reset_token != reset_token:
                abort(403)
            AUTH.update_password(reset_token, password)
            return {"email": eamil, "message": "Password updated"}
        except NoResultFound:
            abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
