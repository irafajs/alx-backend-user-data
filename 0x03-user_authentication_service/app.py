#!/usr/bin/env python3
"""
Shebang to create a py script
"""


from auth import Auth
from flask import Flask, jsonify, request

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
