"""Public user registration using the existing MySQL schema and domain models."""

from __future__ import annotations

import re
from typing import Any

try:  # Support both package imports and the repository's backend-dir test style.
    from .models import Role, User
except ImportError:  # pragma: no cover - exercised by unittest discovery in backend/
    from models import Role, User


class RegistrationError(Exception):
    """Base class for safe registration failures."""


class InvalidRegistrationData(RegistrationError, ValueError):
    """Registration input is missing or invalid."""


class EmailAlreadyRegistered(RegistrationError):
    """The requested email address is already in use."""


class DefaultRoleMissing(RegistrationError):
    """The required Volunteer row is absent from the roles table."""


class RegistrationDatabaseError(RegistrationError):
    """The database could not complete registration."""


_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
_ROLE_SQL = "SELECT role_id, role_name FROM roles WHERE role_name = ?"
_EMAIL_SQL = "SELECT user_id FROM users WHERE email = ?"
_INSERT_SQL = (
    "INSERT INTO users (full_name, email, password_hash, role_id) "
    "VALUES (?, ?, ?, ?)"
)
_USER_SQL = (
    "SELECT user_id, full_name, email, password_hash, role_id, created_at, updated_at "
    "FROM users WHERE user_id = ?"
)


def _mapping(row: Any, columns: tuple[str, ...]) -> dict[str, Any]:
    if isinstance(row, dict):
        return row
    if hasattr(row, "keys"):
        return {key: row[key] for key in row.keys()}
    return dict(zip(columns, row))


def _is_duplicate_key(error: Exception) -> bool:
    # MySQL duplicate-entry error is 1062 (SQLSTATE 23000). Restrict the
    # message fallback to duplicate/unique wording for common DB-API drivers.
    args = getattr(error, "args", ())
    if args and args[0] == 1062:
        return True
    if getattr(error, "sqlstate", None) == "23000" and "duplicate" in str(error).lower():
        return True
    message = str(error).lower()
    return "duplicate entry" in message or "unique constraint failed" in message


class RegistrationService:
    """Register a user on a caller-provided DB-API MySQL connection.

    The connection is injected because this repository has SQL definitions but
    no configured Python MySQL driver or connection factory. SQL uses the `?`
    placeholders documented in ``src/database/operations.sql``.
    """

    def __init__(self, connection: Any):
        if connection is None:
            raise ValueError("connection is required")
        self._connection = connection

    def register(
        self, full_name: str | None = None, email: str | None = None,
        password: str | None = None, **extra: Any,
    ) -> dict[str, Any]:
        """Create a Volunteer account and return its safe public representation.

        Any unrecognized fields (including a client-supplied role) are rejected
        so public callers cannot influence privileged role assignment.
        """
        if extra:
            raise InvalidRegistrationData("unsupported registration field")
        try:
            name = self._validate_name(full_name)
            normalized_email = self._validate_email(email)
            self._validate_password(password)
        except (TypeError, ValueError) as error:
            raise InvalidRegistrationData(str(error)) from error

        cursor = None
        try:
            cursor = self._connection.cursor()
            cursor.execute(_ROLE_SQL, ("Volunteer",))
            role_row = cursor.fetchone()
            if role_row is None:
                raise DefaultRoleMissing("Volunteer role is not configured")
            role_values = _mapping(role_row, ("role_id", "role_name"))
            role = Role.from_record(role_values)
            if role.role_name != "Volunteer":
                raise RegistrationDatabaseError("database returned an invalid default role")

            cursor.execute(_EMAIL_SQL, (normalized_email,))
            if cursor.fetchone() is not None:
                raise EmailAlreadyRegistered("email is already registered")

            user = User.create(name, normalized_email, password, role)
            cursor.execute(_INSERT_SQL, (user.full_name, user.email, user.password_hash, role.role_id))
            user_id = getattr(cursor, "lastrowid", None)
            if not user_id:
                raise RegistrationDatabaseError("database did not return the new user id")
            cursor.execute(_USER_SQL, (user_id,))
            user_row = cursor.fetchone()
            if user_row is None:
                # Drivers may not expose a SELECT-after-insert row until commit;
                # the known safe values still form a valid response.
                user.user_id = int(user_id)
                self._connection.commit()
                return user.to_dict()
            record = _mapping(
                user_row,
                ("user_id", "full_name", "email", "password_hash", "role_id", "created_at", "updated_at"),
            )
            persisted = User.from_record(record, role)
            self._connection.commit()
            return persisted.to_dict()
        except RegistrationError:
            self._safe_rollback()
            raise
        except Exception as error:
            self._safe_rollback()
            if _is_duplicate_key(error):
                raise EmailAlreadyRegistered("email is already registered") from error
            raise RegistrationDatabaseError("registration could not be completed") from error
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
    def _validate_name(value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("full_name is required")
        value = value.strip()
        if len(value) > 150:
            raise ValueError("full_name must be at most 150 characters")
        return value

    @staticmethod
    def _validate_email(value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("email is required")
        value = value.strip().lower()
        if len(value) > 254 or not _EMAIL_RE.fullmatch(value):
            raise ValueError("email must be a valid email address")
        return value

    @staticmethod
    def _validate_password(value: str) -> None:
        # Requirements define strong salted hashing but no password complexity
        # policy. Match the model's minimum (nonempty) rather than invent one.
        if not isinstance(value, str) or not value:
            raise ValueError("password is required")


__all__ = [
    "DefaultRoleMissing", "EmailAlreadyRegistered", "InvalidRegistrationData",
    "RegistrationDatabaseError", "RegistrationError", "RegistrationService",
]
