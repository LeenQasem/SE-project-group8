"""Explicit, guarded creation of the first administrator account."""

from __future__ import annotations

import re
from typing import Any

try:
    from .models import Role, User, hash_password
except ImportError:  # pragma: no cover - backend-dir test discovery
    from models import Role, User, hash_password


_ROLE_SQL = "SELECT role_id, role_name FROM roles WHERE role_name = ? FOR UPDATE"
_ADMIN_COUNT_SQL = (
    "SELECT COUNT(*) FROM users AS u JOIN roles AS r ON r.role_id = u.role_id "
    "WHERE r.role_name = ?"
)
_INSERT_SQL = "INSERT INTO users (full_name, email, password_hash, role_id) VALUES (?, ?, ?, ?)"
_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class BootstrapAdminError(Exception):
    """Bootstrap could not be safely completed."""


def create_initial_admin(connection: Any, full_name: str, email: str, password: str) -> dict | None:
    """Create the first administrator, returning its safe public user record.

    Returns ``None`` when an administrator already exists. Hashing is always
    performed by the backend scrypt password hashing function.
    """
    if connection is None:
        raise ValueError("connection is required")
    if not isinstance(full_name, str) or not full_name.strip() or len(full_name.strip()) > 150:
        raise ValueError("full_name must be nonempty and at most 150 characters")
    if not isinstance(email, str) or not _EMAIL_RE.fullmatch(email.strip()):
        raise ValueError("email must be a valid email address")
    # Generate a secure hash before touching the database; plaintext is never
    # sent to SQL or retained by this helper.
    password_hash = hash_password(password)
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(_ROLE_SQL, ("Administrator",))
        role_row = cursor.fetchone()
        if role_row is None:
            raise BootstrapAdminError("Administrator role is not configured")
        if not isinstance(role_row, dict):
            role_row = dict(zip(("role_id", "role_name"), role_row))
        role = Role.from_record(role_row)
        cursor.execute(_ADMIN_COUNT_SQL, ("Administrator",))
        result = cursor.fetchone()
        count = next(iter(result.values())) if isinstance(result, dict) else result[0]
        if count:
            connection.rollback()
            return None
        cursor.execute(_INSERT_SQL, (full_name.strip(), email.strip().lower(), password_hash, role.role_id))
        connection.commit()
        user_id = getattr(cursor, "lastrowid", None)
        user = User(user_id, full_name.strip(), email.strip().lower(), password_hash, role)
        return user.to_dict()
    except BootstrapAdminError:
        try:
            connection.rollback()
        except Exception:
            pass
        raise
    except Exception as error:
        try:
            connection.rollback()
        except Exception:
            pass
        raise BootstrapAdminError("initial administrator could not be created") from error
    finally:
        if cursor is not None:
            try:
                cursor.close()
            except Exception:
                pass


__all__ = ["BootstrapAdminError", "create_initial_admin"]
