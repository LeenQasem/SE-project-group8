"""Server-side role checks for authenticated principals."""

from __future__ import annotations

from enum import Enum

try:
    from .models import User
except ImportError:  # pragma: no cover
    from models import User


class UserRole(str, Enum):
    ADMINISTRATOR = "Administrator"
    EVENT_ORGANIZER = "Event Organizer"
    VOLUNTEER = "Volunteer"


class AuthorizationError(PermissionError):
    """Caller is unauthenticated or lacks the required role."""


def require_role(user: User | None, role: UserRole | str) -> User:
    if not isinstance(user, User):
        raise AuthorizationError("authentication is required")
    role_name = role.value if isinstance(role, UserRole) else role
    if not user.has_role(role_name):
        raise AuthorizationError("required role is missing")
    return user


def require_admin(user: User | None) -> User:
    return require_role(user, UserRole.ADMINISTRATOR)


def authenticate_and_require_role(login_service, token: str | None, role: UserRole | str) -> User:
    """Resolve the bearer token through LoginService, then enforce its role."""
    if login_service is None or not isinstance(token, str) or not token:
        raise AuthorizationError("authentication is required")
    user = login_service.authenticate_token(token)
    return require_role(user, role)


def authenticate_and_require_admin(login_service, token: str | None) -> User:
    return authenticate_and_require_role(login_service, token, UserRole.ADMINISTRATOR)


__all__ = ["AuthorizationError", "UserRole", "authenticate_and_require_admin",
           "authenticate_and_require_role", "require_admin", "require_role"]
