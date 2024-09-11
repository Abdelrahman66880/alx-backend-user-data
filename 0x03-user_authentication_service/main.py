#!/usr/bin/env python3
import requests

BASE_URL = "http://localhost:5000"

def register_user(email: str, password: str) -> None:
    response = requests.post(f"{BASE_URL}/users", json={"email": email, "password": password})
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    print("User registered successfully")

def log_in_wrong_password(email: str, password: str) -> None:
    response = requests.post(f"{BASE_URL}/sessions", json={"email": email, "password": password})
    assert response.status_code == 401, f"Expected status 401, got {response.status_code}"
    print("Login with wrong password failed as expected")

def log_in(email: str, password: str) -> str:
    response = requests.post(f"{BASE_URL}/sessions", json={"email": email, "password": password})
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    session_id = response.cookies.get("session_id")
    print("Logged in successfully")
    return session_id

def profile_unlogged() -> None:
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, f"Expected status 403, got {response.status_code}"
    print("Profile access while unlogged failed as expected")

def profile_logged(session_id: str) -> None:
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    print("Profile accessed successfully while logged in")

def log_out(session_id: str) -> None:
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    print("Logged out successfully")

def reset_password_token(email: str) -> str:
    response = requests.post(f"{BASE_URL}/reset_password", json={"email": email})
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    reset_token = response.json().get("reset_token")
    print("Password reset token received")
    return reset_token

def update_password(email: str, reset_token: str, new_password: str) -> None:
    response = requests.put(f"{BASE_URL}/reset_password", json={
        "email": email, "reset_token": reset_token, "new_password": new_password
    })
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    print("Password updated successfully")


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

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