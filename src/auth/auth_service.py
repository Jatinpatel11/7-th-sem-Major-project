"""
Authentication service for user management and session handling.
"""
import json
import os
from datetime import datetime
from typing import Optional, Dict
import bcrypt
import streamlit as st


class AuthService:
    """Handles user authentication, creation, and session management."""
    
    def __init__(self, users_file: str = "data/users.json"):
        """Initialize the authentication service.
        
        Args:
            users_file: Path to the JSON file storing user credentials
        """
        self.users_file = users_file
        self._ensure_users_file()
    
    def _ensure_users_file(self):
        """Create users file if it doesn't exist."""
        if not os.path.exists(self.users_file):
            os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
    
    def _load_users(self) -> Dict:
        """Load users from JSON file."""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_users(self, users: Dict):
        """Save users to JSON file."""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password as string
        """
        # Cost factor of 12 for security
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash.
        
        Args:
            password: Plain text password to verify
            hashed: Hashed password to compare against
            
        Returns:
            True if password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def create_user(self, username: str, password: str) -> tuple[bool, str]:
        """Create a new user account.
        
        Args:
            username: Username for the new account
            password: Password for the new account
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not username or not password:
            return False, "Username and password are required"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        users = self._load_users()
        
        if username in users:
            return False, "Username already exists"
        
        # Create new user
        users[username] = {
            "password_hash": self.hash_password(password),
            "created_at": datetime.now().isoformat(),
            "last_login": None
        }
        
        self._save_users(users)
        return True, "User created successfully"
    
    def authenticate_user(self, username: str, password: str) -> tuple[bool, str]:
        """Authenticate a user with username and password.
        
        Args:
            username: Username to authenticate
            password: Password to verify
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not username or not password:
            return False, "Username and password are required"
        
        users = self._load_users()
        
        if username not in users:
            return False, "Invalid username or password"
        
        user_data = users[username]
        
        if not self.verify_password(password, user_data["password_hash"]):
            return False, "Invalid username or password"
        
        # Update last login
        users[username]["last_login"] = datetime.now().isoformat()
        self._save_users(users)
        
        return True, "Login successful"
    
    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated.
        
        Returns:
            True if user is authenticated, False otherwise
        """
        return st.session_state.get("authenticated", False)
    
    def get_current_user(self) -> Optional[str]:
        """Get the currently authenticated username.
        
        Returns:
            Username if authenticated, None otherwise
        """
        if self.is_authenticated():
            return st.session_state.get("username")
        return None
    
    def login(self, username: str):
        """Set session state for logged in user.
        
        Args:
            username: Username to log in
        """
        st.session_state["authenticated"] = True
        st.session_state["username"] = username
    
    def logout(self):
        """Clear session state and log out user."""
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        # Clear other session data
        for key in list(st.session_state.keys()):
            if key not in ["authenticated", "username"]:
                del st.session_state[key]


# Global instance
auth_service = AuthService()
