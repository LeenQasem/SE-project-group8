"""User profile and administrator account management for Increment 1."""

from __future__ import annotations

import re
from typing import Any

try:
    from .models import Role, User
except ImportError:  # pragma: no cover - backend-dir test discovery
    from models import Role, User


class UserManagementError(Exception):
    """Base class for safe user-management failures."""


class InvalidUserManagementData(UserManagementError, ValueError):
    """An identifier or profile value is invalid."""


class UserNotFound(UserManagementError):
    """The requested account does not exist."""


class UnauthorizedUserManagement(UserManagementError, PermissionError):
    """The authenticated principal cannot perform the operation."""


class EmailAlreadyInUse(UserManagementError):
    """The requested email is already assigned to another account."""


class UserManagementDatabaseError(UserManagementError):
    """Persistence failed; database details are deliberately hidden."""


_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
_USER_COLUMNS = ("user_id", "full_name", "email", "password_hash", "role_id", "created_at", "updated_at", "role_name")
_SELECT_ONE = (
    "SELECT u.user_id, u.full_name, u.email, u.password_hash, u.role_id, "
    "u.created_at, u.updated_at, r.role_name FROM users AS u "
    "JOIN roles AS r ON r.role_id = u.role_id WHERE u.user_id = ?"
)
_SELECT_ALL = (
    "SELECT u.user_id, u.full_name, u.email, u.password_hash, u.role_id, "
    "u.created_at, u.updated_at, r.role_name FROM users AS u "
    "JOIN roles AS r ON r.role_id = u.role_id ORDER BY u.user_id LIMIT ? OFFSET ?"
)
_EMAIL_OWNER = "SELECT user_id FROM users WHERE email = ? AND user_id <> ?"
_UPDATE_PROFILE = "UPDATE users SET full_name = ?, email = ? WHERE user_id = ?"


def _mapping(row: Any) -> dict[str, Any]:
    if isinstance(row, dict):
        return row
    if hasattr(row, "keys"):
        return {key: row[key] for key in row.keys()}
    return dict(zip(_USER_COLUMNS, row))


class UserManagementService:
    """Manage safe profile data on an injected DB-API connection.

    ``actor_id`` and ``actor_role`` are trusted authentication context supplied
    by the future controller/session-validation layer, never request fields.
    This repository does not yet implement that layer. Role assignment is
    intentionally excluded; the approved design assigns it through the
    separate administrator role-management action.
    """

    def __init__(self, connection: Any):
        if connection is None:
            raise ValueError("connection is required")
        self._connection = connection

    def get_user(self, user_id: int, *, actor_id: int, actor_role: str) -> dict[str, Any]:
        target = self._validate_id(user_id, "user_id")
        caller = self._validate_id(actor_id, "actor_id")
        self._authorize_profile_read(caller, actor_role, target)
        return self._fetch_one(target)

    def get_my_profile(self, *, actor_id: int) -> dict[str, Any]:
        caller = self._validate_id(actor_id, "actor_id")
        return self._fetch_one(caller)

    def list_users(self, *, actor_id: int, actor_role: str, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
        self._require_admin(actor_id, actor_role)
        if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 500:
            raise InvalidUserManagementData("limit must be an integer from 1 to 500")
        if not isinstance(offset, int) or isinstance(offset, bool) or offset < 0:
            raise InvalidUserManagementData("offset must be a non-negative integer")
        return self._query(_SELECT_ALL, (limit, offset), many=True)

    def update_profile(self, user_id: int, changes: dict[str, Any], *, actor_id: int, actor_role: str) -> dict[str, Any]:
        target = self._validate_id(user_id, "user_id")
        caller = self._validate_id(actor_id, "actor_id")
        if not isinstance(changes, dict) or not changes:
            raise InvalidUserManagementData("at least one profile field is required")
        if any(key not in {"full_name", "email"} for key in changes):
            raise InvalidUserManagementData("only full_name and email may be updated")
        if caller != target and actor_role != "Administrator":
            raise UnauthorizedUserManagement("not authorized to update this account")
        if actor_role not in {"Administrator", "Event Organizer", "Volunteer"}:
            raise UnauthorizedUserManagement("not authorized to update this account")

        current = self._fetch_record(target)
        name = self._validate_name(changes.get("full_name", current["full_name"]))
        email = self._validate_email(changes.get("email", current["email"]))
        if email != current["email"]:
            self._check_email_available(email, target)
        self._query(_UPDATE_PROFILE, (name, email, target), commit=True)
        return self._fetch_one(target)

    def _fetch_one(self, user_id: int) -> dict[str, Any]:
        record = self._fetch_record(user_id)
        role = Role.from_record({"role_id": record["role_id"], "role_name": record["role_name"]})
        user = User.from_record(record, role)
        return user.to_dict()

    def _fetch_record(self, user_id: int) -> dict[str, Any]:
        rows = self._query(_SELECT_ONE, (user_id,), one=True)
        if rows is None:
            raise UserNotFound("user was not found")
        return rows

    def _check_email_available(self, email: str, user_id: int) -> None:
        if self._query(_EMAIL_OWNER, (email, user_id), one=True) is not None:
            raise EmailAlreadyInUse("email address is already in use")

    def _query(self, sql: str, params: tuple, *, one: bool = False, many: bool = False, commit: bool = False):
        cursor = None
        try:
            cursor = self._connection.cursor()
            cursor.execute(sql, params)
            result = cursor.fetchall() if many else cursor.fetchone() if one else None
            if commit:
                self._connection.commit()
            if many:
                return [self._public_record(row) for row in result]
            return _mapping(result) if one and result is not None else result
        except UserManagementError:
            raise
        except Exception as error:
            try:
                self._connection.rollback()
            except Exception:
                pass
            if _is_duplicate(error):
                raise EmailAlreadyInUse("email address is already in use") from error
            raise UserManagementDatabaseError("user management request could not be completed") from error
        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass

    @staticmethod
    def _public_record(row: Any) -> dict[str, Any]:
        record = _mapping(row)
        role = Role.from_record({"role_id": record["role_id"], "role_name": record["role_name"]})
        return User.from_record(record, role).to_dict()

    @staticmethod
    def _validate_id(value: int, field: str) -> int:
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise InvalidUserManagementData(f"{field} must be a positive integer")
        return value

    @staticmethod
    def _require_admin(actor_id: int, actor_role: str) -> None:
        UserManagementService._validate_id(actor_id, "actor_id")
        if actor_role != "Administrator":
            raise UnauthorizedUserManagement("administrator access is required")

    @staticmethod
    def _authorize_profile_read(actor_id: int, actor_role: str, target_id: int) -> None:
        if actor_id != target_id and actor_role != "Administrator":
            raise UnauthorizedUserManagement("not authorized to view this account")

    @staticmethod
    def _validate_name(value: Any) -> str:
        if not isinstance(value, str) or not value.strip() or len(value.strip()) > 150:
            raise InvalidUserManagementData("full_name must be nonempty and at most 150 characters")
        return value.strip()

    @staticmethod
    def _validate_email(value: Any) -> str:
        if not isinstance(value, str) or not value.strip():
            raise InvalidUserManagementData("email is required")
        normalized = value.strip().lower()
        if len(normalized) > 254 or not _EMAIL_RE.fullmatch(normalized):
            raise InvalidUserManagementData("email must be a valid email address")
        return normalized


def _is_duplicate(error: Exception) -> bool:
    args = getattr(error, "args", ())
    return bool(args and args[0] == 1062) or "duplicate entry" in str(error).lower() or "unique constraint failed" in str(error).lower()


__all__ = [
    "EmailAlreadyInUse", "InvalidUserManagementData", "UnauthorizedUserManagement",
    "UserManagementDatabaseError", "UserManagementError", "UserManagementService", "UserNotFound",
]
