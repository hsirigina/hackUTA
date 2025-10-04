"""Decorators for role-based access control."""
import streamlit as st
from functools import wraps
from typing import Callable, Optional
from auth.session import session


def require_auth(func: Callable) -> Callable:
    """Decorator to require authentication for a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.is_authenticated():
            st.warning("🔒 Please log in to access this page.")
            st.stop()
        return func(*args, **kwargs)
    return wrapper


def require_role(role: str) -> Callable:
    """Decorator to require a specific role for a function."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not session.is_authenticated():
                st.warning("🔒 Please log in to access this page.")
                st.stop()

            user_role = session.get_user_role()
            if user_role != role:
                st.error(f"⛔ Access denied. This page requires '{role}' role.")
                st.stop()

            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_supervisor(func: Callable) -> Callable:
    """Decorator to require supervisor role."""
    return require_role('supervisor')(func)


def require_driver(func: Callable) -> Callable:
    """Decorator to require driver role."""
    return require_role('driver')(func)


def show_for_role(role: str) -> Callable:
    """
    Decorator to show content only for specific role.
    Returns None if user doesn't have the required role.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not session.is_authenticated():
                return None

            user_role = session.get_user_role()
            if user_role != role:
                return None

            return func(*args, **kwargs)
        return wrapper
    return decorator


def show_for_supervisor(func: Callable) -> Callable:
    """Decorator to show content only for supervisors."""
    return show_for_role('supervisor')(func)


def show_for_driver(func: Callable) -> Callable:
    """Decorator to show content only for drivers."""
    return show_for_role('driver')(func)
