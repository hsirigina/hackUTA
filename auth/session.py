"""Session management for Streamlit with Auth0."""
import streamlit as st
from typing import Optional, Dict, Any
from auth.auth0_config import auth0_config


class SessionManager:
    """Manage authentication sessions in Streamlit."""

    @staticmethod
    def is_authenticated() -> bool:
        """Check if user is authenticated."""
        return 'user' in st.session_state and st.session_state.user is not None

    @staticmethod
    def get_user() -> Optional[Dict[str, Any]]:
        """Get the current authenticated user."""
        return st.session_state.get('user')

    @staticmethod
    def get_user_role() -> Optional[str]:
        """Get the current user's role."""
        user = SessionManager.get_user()
        if user:
            return user.get('role', 'driver')
        return None

    @staticmethod
    def is_supervisor() -> bool:
        """Check if current user is a supervisor."""
        return SessionManager.get_user_role() == 'supervisor'

    @staticmethod
    def is_driver() -> bool:
        """Check if current user is a driver."""
        return SessionManager.get_user_role() == 'driver'

    @staticmethod
    def get_supervised_users() -> list:
        """Get list of users supervised by current user."""
        user = SessionManager.get_user()
        if user and SessionManager.is_supervisor():
            return user.get('supervised_users', [])
        return []

    @staticmethod
    def get_supervisor_id() -> Optional[str]:
        """Get the supervisor ID for the current driver."""
        user = SessionManager.get_user()
        if user and SessionManager.is_driver():
            return user.get('supervisor_id')
        return None

    @staticmethod
    def set_user(user_info: Dict[str, Any], token: Dict[str, Any]):
        """Set the authenticated user in session."""
        st.session_state.user = user_info
        st.session_state.token = token
        st.session_state.authenticated = True

    @staticmethod
    def clear_session():
        """Clear the authentication session."""
        if 'user' in st.session_state:
            del st.session_state.user
        if 'token' in st.session_state:
            del st.session_state.token
        if 'authenticated' in st.session_state:
            del st.session_state.authenticated
        if 'oauth_state' in st.session_state:
            del st.session_state.oauth_state

    @staticmethod
    def init_session():
        """Initialize session state variables."""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user' not in st.session_state:
            st.session_state.user = None
        if 'token' not in st.session_state:
            st.session_state.token = None

    @staticmethod
    def login_redirect():
        """Get the login URL and redirect user."""
        authorization_url, state = auth0_config.get_authorization_url()
        st.session_state.oauth_state = state
        return authorization_url

    @staticmethod
    def logout():
        """Log out the current user."""
        SessionManager.clear_session()
        logout_url = auth0_config.get_logout_url()
        return logout_url

    @staticmethod
    def get_user_id() -> Optional[str]:
        """Get the current user's ID."""
        user = SessionManager.get_user()
        if user:
            return user.get('sub') or user.get('user_id')
        return None

    @staticmethod
    def get_user_email() -> Optional[str]:
        """Get the current user's email."""
        user = SessionManager.get_user()
        if user:
            return user.get('email')
        return None

    @staticmethod
    def get_user_name() -> Optional[str]:
        """Get the current user's name."""
        user = SessionManager.get_user()
        if user:
            return user.get('name') or user.get('email', 'User')
        return None


# Convenience instance
session = SessionManager()
