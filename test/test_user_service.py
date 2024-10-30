import pytest
from unittest.mock import patch
from werkzeug.security import generate_password_hash
from utils.auth import AuthService

@patch("database.db_mysql.MySQLDatabase")
def test_register_user(mock_db):
    mock_db_instance = mock_db.return_value
    mock_db_instance.execute_update.return_value = 1

    auth_service = AuthService()
    response, status = auth_service.register_user("test_user", "password123", "user")

    assert status == 201
    assert response["message"] == "User registered successfully"

@patch("database.db_mysql.MySQLDatabase")
def test_register_user_existing(mock_db):
    mock_db_instance = mock_db.return_value
    mock_db_instance.execute_update.return_value = 0

    auth_service = AuthService()
    response, status = auth_service.register_user("test_user", "password123", "user")

    assert status == 400
    assert response["message"] == "Username already taken"

@patch("database.db_mysql.MySQLDatabase")
def test_login_user_success(mock_db):
    mock_db_instance = mock_db.return_value
    mock_db_instance.execute_query.return_value = [
        {"username": "test_user", "password": generate_password_hash("password123"), "role": "user"}
    ]

    auth_service = AuthService()
    response, status = auth_service.login_user("test_user", "password123")

    assert status == 200
    assert "access_token" in response

@patch("database.db_mysql.MySQLDatabase")
def test_login_user_invalid_credentials(mock_db):
    mock_db_instance = mock_db.return_value
    mock_db_instance.execute_query.return_value = []

    auth_service = AuthService()
    response, status = auth_service.login_user("test_user", "wrong_password")

    assert status == 401
    assert response["message"] == "Invalid credentials"
