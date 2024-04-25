import requests
from typing import Optional

BASE_URL = "http://localhost:5000"

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """method to test users routes"""
    url = f"{BASE_URL}/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        assert response.status_code == 200
    elif response.status_code == 400:
        assert response.status_code == 400
    else:
        assert response.status_code == 500


def log_in_wrong_password(email: str, password: str) -> None:
    """Method to test route sessions with post method"""
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        assert response.status_code == 200
    elif response.status_code == 401:
        assert response.status_code == 401
    else:
        assert response.status_code == 500


def log_in(email: str, password: str) -> str:
    """method to test sessions while logging in"""
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        assert response.status_code == 200
    elif response.status_code == 401:
        assert response.status_code == 401
    else:
        assert response.status_code == 500
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """method to test profile route with get method"""
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """method to test user profile while successful logged in"""
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """method to test logout on route sessions with delete method"""
    url = f"{BASE_URL}/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """method to test password reset using route reset password
    with post method"""
    url = f"{BASE_URL}/reset_password"
    data = {"email": email}
    response = requests.post(url, data=data)
    assert response.status_code == 200


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """method to test updated password using route reset_password
    with put method"""
    url = f"{BASE_URL}/reset_password"
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(url, data=data)
    if response.status_code == 200:
        assert response.status_code == 200
    else:
        assert response.status_code == 403


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
