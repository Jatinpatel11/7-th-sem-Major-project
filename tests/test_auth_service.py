"""
Unit tests for authentication service.
"""
import os
import json
import tempfile
import pytest
from src.auth.auth_service import AuthService


@pytest.fixture
def temp_users_file():
    """Create a temporary users file for testing."""
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def auth_service_instance(temp_users_file):
    """Create an AuthService instance with temporary file."""
    return AuthService(users_file=temp_users_file)


def test_create_user_success(auth_service_instance):
    """Test successful user creation."""
    success, message = auth_service_instance.create_user("testuser", "password123")
    assert success is True
    assert "successfully" in message.lower()


def test_create_user_duplicate(auth_service_instance):
    """Test creating duplicate user fails."""
    auth_service_instance.create_user("testuser", "password123")
    success, message = auth_service_instance.create_user("testuser", "password456")
    assert success is False
    assert "already exists" in message.lower()


def test_create_user_short_password(auth_service_instance):
    """Test that short passwords are rejected."""
    success, message = auth_service_instance.create_user("testuser", "12345")
    assert success is False
    assert "6 characters" in message.lower()


def test_create_user_empty_fields(auth_service_instance):
    """Test that empty username or password is rejected."""
    success, message = auth_service_instance.create_user("", "password123")
    assert success is False
    
    success, message = auth_service_instance.create_user("testuser", "")
    assert success is False


def test_authenticate_user_success(auth_service_instance):
    """Test successful authentication."""
    auth_service_instance.create_user("testuser", "password123")
    success, message = auth_service_instance.authenticate_user("testuser", "password123")
    assert success is True
    assert "successful" in message.lower()


def test_authenticate_user_wrong_password(auth_service_instance):
    """Test authentication with wrong password."""
    auth_service_instance.create_user("testuser", "password123")
    success, message = auth_service_instance.authenticate_user("testuser", "wrongpassword")
    assert success is False
    assert "invalid" in message.lower()


def test_authenticate_user_nonexistent(auth_service_instance):
    """Test authentication with non-existent user."""
    success, message = auth_service_instance.authenticate_user("nonexistent", "password123")
    assert success is False
    assert "invalid" in message.lower()


def test_password_hashing(auth_service_instance):
    """Test that passwords are properly hashed."""
    password = "testpassword123"
    hashed = auth_service_instance.hash_password(password)
    
    # Hash should be different from original
    assert hashed != password
    
    # Should be able to verify
    assert auth_service_instance.verify_password(password, hashed) is True
    
    # Wrong password should not verify
    assert auth_service_instance.verify_password("wrongpassword", hashed) is False


def test_users_file_creation(temp_users_file):
    """Test that users file is created if it doesn't exist."""
    # Remove the temp file
    os.unlink(temp_users_file)
    
    # Create auth service - should create the file
    auth_service = AuthService(users_file=temp_users_file)
    
    assert os.path.exists(temp_users_file)


def test_user_data_persistence(auth_service_instance, temp_users_file):
    """Test that user data persists across instances."""
    # Create user with first instance
    auth_service_instance.create_user("testuser", "password123")
    
    # Create new instance with same file
    new_instance = AuthService(users_file=temp_users_file)
    
    # Should be able to authenticate
    success, _ = new_instance.authenticate_user("testuser", "password123")
    assert success is True


def test_last_login_update(auth_service_instance, temp_users_file):
    """Test that last login timestamp is updated."""
    auth_service_instance.create_user("testuser", "password123")
    
    # Load users and check last_login is None
    with open(temp_users_file, 'r') as f:
        users = json.load(f)
    assert users["testuser"]["last_login"] is None
    
    # Authenticate
    auth_service_instance.authenticate_user("testuser", "password123")
    
    # Load users and check last_login is updated
    with open(temp_users_file, 'r') as f:
        users = json.load(f)
    assert users["testuser"]["last_login"] is not None
