"""User login and persisted-session creation for the Increment 1 backend."""

from __future__ import annotations

import re
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

try:
    from .models import Role, User, UserSession
except ImportError:  # pragma: no cover - supports discovery from backend/
    from models import Role, User, UserSession


class LoginError(Exception):
    """Base class for safe login failures."""


class InvalidLoginData(LoginError, ValueError):
    """Login input is missing or malformed."""


class InvalidCredentials(LoginError):
    """The supplied email and password do not authenticate a user."""


class LoginDatabaseError(LoginError):
    """The database could not complete authentication."""


class SessionCreationError(LoginError):
    """A persisted authenticated session could not be created."""


_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
_USER_SQL = (
    "SELECT u.user_id, u.full_name, u.email, u.password_hash, u.role_id, "
    "u.created_at, u.updated_at, r.role_name FROM users AS u "
    "JOIN roles AS r ON r.role_id = u.role_id WHERE u.email = ?"
)
_SESSION_SQL = "INSERT INTO user_sessions (user_id, token_hash, expires_at) VALUES (?, ?, ?)"
_AUTHENTICATE_TOKEN_SQL = (
    "SELECT u.user_id, u.full_name, u.email, u.password_hash, u.role_id, "
    "u.created_at, u.updated_at, r.role_name FROM user_sessions AS s "
    "JOIN users AS u ON u.user_id = s.user_id JOIN roles AS r ON r.role_id = u.role_id "
    "WHERE s.token_hash = ? AND s.revoked_at IS NULL AND s.expires_at > CURRENT_TIMESTAMP"
)


def _mapping(row: Any, columns: tuple[str, ...]) -> dict[str, Any]:
    if isinstance(row, dict):
        return row
    if hasattr(row, "keys"):
        return {key: row[key] for key in row.keys()}
    return dict(zip(columns, row))


class LoginService:
    """Authenticate using an injected DB-API connection and persist a session.

    The database stores only the SHA-256 digest of an opaque bearer token. The
    default session lifetime is 12 hours and can be set by application config.
    """

    def __init__(self, connection: Any, session_lifetime: timedelta = timedelta(hours=12)):
        if connection is None:
            raise ValueError("connection is required")
        if not isinstance(session_lifetime, timedelta) or session_lifetime <= timedelta(0):
            raise ValueError("session_lifetime must be a positive timedelta")
        self._connection = connection
        self._session_lifetime = session_lifetime

    def login(self, email: str | None = None, password: str | None = None) -> dict[str, Any]:
        normalized_email = self._validate_email(email)
        self._validate_password(password)
        cursor = None
        try:
            cursor = self._connection.cursor()
            cursor.execute(_USER_SQL, (normalized_email,))
            row = cursor.fetchone()
            if row is None:
                raise InvalidCredentials("email or password is incorrect")

            record = _mapping(
                row,
                ("user_id", "full_name", "email", "password_hash", "role_id", "created_at", "updated_at", "role_name"),
            )
            role = Role.from_record({"role_id": record["role_id"], "role_name": record["role_name"]})
            user = User.from_record(record, role)
            if not user.verify_password(password):
                raise InvalidCredentials("email or password is incorrect")

            # MySQL DATETIME is timezone-naive in this schema; store UTC values.
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            expires_at = now + self._session_lifetime
            token = secrets.token_urlsafe(32)
            session = UserSession.create(user.user_id, token, expires_at)
            try:
                cursor.execute(_SESSION_SQL, (user.user_id, session.token_hash, expires_at))
                self._connection.commit()
            except Exception as error:
                raise SessionCreationError("authenticated session could not be created") from error
            return {"user": user.to_dict(), "access_token": token, "expires_at": expires_at}
        except LoginError:
            self._safe_rollback()
            raise
        except Exception as error:
            self._safe_rollback()
            # Keep DB and unexpected authentication internals out of client errors.
            raise LoginDatabaseError("login could not be completed") from error
        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass

    def authenticate_token(self, token: str | None) -> User | None:
        """Resolve an active bearer token to its current persisted user role."""
        if not isinstance(token, str) or not token:
            return None
        cursor = None
        try:
            cursor = self._connection.cursor()
            cursor.execute(_AUTHENTICATE_TOKEN_SQL, (UserSession.digest_token(token),))
            row = cursor.fetchone()
            if row is None:
                return None
            record = _mapping(row, ("user_id", "full_name", "email", "password_hash", "role_id", "created_at", "updated_at", "role_name"))
            role = Role.from_record({"role_id": record["role_id"], "role_name": record["role_name"]})
            return User.from_record(record, role)
        except Exception as error:
            self._safe_rollback()
            raise LoginDatabaseError("token authentication could not be completed") from error
        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass

    def _safe_rollback(self) -> None:
        try:
            self._connection.rollback()
        except Exception:
            pass

    @staticmethod
    def _validate_email(value: str | None) -> str:
        if not isinstance(value, str) or not value.strip():
            raise InvalidLoginData("email is required")
        value = value.strip().lower()
        if len(value) > 254 or not _EMAIL_RE.fullmatch(value):
            raise InvalidLoginData("email must be a valid email address")
        return value

    @staticmethod
    def _validate_password(value: str | None) -> None:
        if not isinstance(value, str) or not value:
            raise InvalidLoginData("password is required")
        if len(value) > 1024:
            raise InvalidLoginData("password is too long")


__all__ = [
    "InvalidCredentials", "InvalidLoginData", "LoginDatabaseError", "LoginError",
    "LoginService", "SessionCreationError",
]
