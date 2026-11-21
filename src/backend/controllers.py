"""Increment 1 controllers coordinating authentication and user management."""

from __future__ import annotations

try:
    from .login_service import LoginService
    from .rbac import AuthorizationError, authenticate_and_require_admin
    from .registration_service import RegistrationService
    from .user_management_service import UserManagementService
except ImportError:  # unittest discovery with src/backend on sys.path
    from login_service import LoginService
    from rbac import AuthorizationError, authenticate_and_require_admin
    from registration_service import RegistrationService
    from user_management_service import UserManagementService


def _safe(value):
    """Defensively remove credential digests from controller responses."""
    if isinstance(value, dict):
        return {key: _safe(item) for key, item in value.items() if key not in {"password_hash", "token_hash"}}
    if isinstance(value, list):
        return [_safe(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_safe(item) for item in value)
    return value


class AuthController:
    """Expose safe authentication operations through the service layer."""

    def __init__(self, registration_service: RegistrationService, login_service: LoginService, connection=None):
        self.registration_service = registration_service
        self.login_service = login_service
        self.connection = connection or getattr(registration_service, "_connection", None)

    def register(self, name: str, email: str, password: str) -> dict:
        return _safe(self.registration_service.register(full_name=name, email=email, password=password))

    def login(self, email: str, password: str) -> dict:
        result = self.login_service.login(email=email, password=password)
        return _safe({"user": result["user"], "access_token": result["access_token"], "expires_at": result["expires_at"]})

    def logout(self, token: str) -> None:
        """Revoke an active token by its digest; never persist the bearer token."""
        from datetime import datetime, timezone
        try:
            from .models import UserSession
        except ImportError:  # pragma: no cover
            from models import UserSession
        if not isinstance(token, str) or not token:
            raise ValueError("authentication token is required")
        if self.connection is None:
            raise RuntimeError("session persistence is unavailable")
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "UPDATE user_sessions SET revoked_at = ? WHERE token_hash = ? AND revoked_at IS NULL",
                (datetime.now(timezone.utc).replace(tzinfo=None), UserSession.digest_token(token)),
            )
            self.connection.commit()
        except Exception as error:
            try:
                self.connection.rollback()
            except Exception:
                pass
            raise RuntimeError("logout could not be completed") from error
        finally:
            try:
                cursor.close()
            except Exception:
                pass


class AdminUserController:
    """Resolve bearer credentials and delegate administrator operations."""

    def __init__(self, login_service: LoginService, user_management_service: UserManagementService):
        self.login_service = login_service
        self.user_management_service = user_management_service

    def _admin(self, token: str):
        return authenticate_and_require_admin(self.login_service, token)

    def view_users(self, token: str) -> list[dict]:
        return _safe(self.user_management_service.view_users(self._admin(token)))

    def assign_role(self, token: str, user_id: int, role: str) -> dict:
        return _safe(self.user_management_service.assign_role(self._admin(token), user_id, role))


__all__ = ["AdminUserController", "AuthController"]
