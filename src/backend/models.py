"""Validated domain models matching ``src/database/schema.sql``.

Persistence is intentionally left to the application's MySQL data-access
layer. These models accept database IDs and provide record conversion helpers
so a DB-API adapter can map rows without introducing an ORM dependency.
"""

from __future__ import annotations

import hashlib
import hmac
import re
import secrets
from dataclasses import dataclass, field
from datetime import datetime


_ROLE_NAMES = frozenset({"Administrator", "Event Organizer", "Volunteer"})
_ROLE_ALIASES = {"ADMINISTRATOR": "Administrator", "EVENT_ORGANIZER": "Event Organizer", "VOLUNTEER": "Volunteer"}
_TOKEN_HASH_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_PASSWORD_HASH_PREFIX = "scrypt"


def _required_text(value: str, field_name: str, max_length: int) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")
    value = value.strip()
    if len(value) > max_length:
        raise ValueError(f"{field_name} must be at most {max_length} characters")
    return value


def _is_timezone_aware(value: datetime) -> bool:
    return value.utcoffset() is not None


def _require_matching_timezone_awareness(*values: datetime | None) -> None:
    awareness = {_is_timezone_aware(value) for value in values if value is not None}
    if len(awareness) > 1:
        raise ValueError("datetime values must be consistently timezone-aware or timezone-naive")


def hash_password(password: str) -> str:
    """Return a salted scrypt password hash; plaintext is never retained."""
    if not isinstance(password, str) or not password:
        raise ValueError("password is required")
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
    return f"{_PASSWORD_HASH_PREFIX}${salt.hex()}${digest.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against a hash emitted by :func:`hash_password`."""
    try:
        algorithm, salt_hex, digest_hex = password_hash.split("$", 2)
        if algorithm != _PASSWORD_HASH_PREFIX:
            return False
        salt, expected = bytes.fromhex(salt_hex), bytes.fromhex(digest_hex)
        if len(salt) != 16 or len(expected) != 64:
            return False
        actual = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
        return hmac.compare_digest(actual, expected)
    except (AttributeError, TypeError, ValueError):
        return False


@dataclass(frozen=True, slots=True)
class Role:
    """A row in ``roles``; role names are constrained by the schema."""

    role_id: int
    role_name: str

    def __post_init__(self) -> None:
        if not isinstance(self.role_id, int) or isinstance(self.role_id, bool) or self.role_id <= 0:
            raise ValueError("role_id must be a positive integer")
        if self.role_name not in _ROLE_NAMES:
            raise ValueError("role_name must be one of the seeded role names")

    @classmethod
    def from_record(cls, row: dict) -> Role:
        return cls(role_id=row["role_id"], role_name=row["role_name"])

    def to_dict(self) -> dict:
        return {"role_id": self.role_id, "role_name": self.role_name}


@dataclass(slots=True)
class User:
    """A user row with one required Role and zero or more UserSessions."""

    user_id: int | None
    full_name: str
    email: str
    password_hash: str = field(repr=False)
    role: Role
    created_at: datetime | None = None
    updated_at: datetime | None = None
    sessions: list[UserSession] = field(default_factory=list, repr=False)

    def __post_init__(self) -> None:
        if self.user_id is not None and (
            not isinstance(self.user_id, int) or isinstance(self.user_id, bool) or self.user_id <= 0
        ):
            raise ValueError("user_id must be a positive integer when provided")
        self.full_name = _required_text(self.full_name, "full_name", 150)
        self.email = _required_text(self.email, "email", 254)
        if "@" not in self.email or self.email.startswith("@") or self.email.endswith("@"):
            raise ValueError("email must be a valid email address")
        if not isinstance(self.password_hash, str) or not self.password_hash or len(self.password_hash) > 255:
            raise ValueError("password_hash must be nonempty and at most 255 characters")
        if not isinstance(self.role, Role):
            raise ValueError("role must be a Role")
        if self.created_at is not None and not isinstance(self.created_at, datetime):
            raise ValueError("created_at must be a datetime or None")
        if self.updated_at is not None and not isinstance(self.updated_at, datetime):
            raise ValueError("updated_at must be a datetime or None")
        _require_matching_timezone_awareness(self.created_at, self.updated_at)
        for session in self.sessions:
            if session.user_id != self.user_id:
                raise ValueError("session user_id must match the owning user")

    @classmethod
    def create(cls, full_name: str, email: str, password: str, role: Role) -> User:
        return cls(None, full_name, email, hash_password(password), role)

    @classmethod
    def from_record(cls, row: dict, role: Role) -> User:
        return cls(
            user_id=row["user_id"], full_name=row["full_name"], email=row["email"],
            password_hash=row["password_hash"], role=role,
            created_at=row.get("created_at"), updated_at=row.get("updated_at"),
        )

    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.password_hash)

    def has_role(self, role: str | Role) -> bool:
        """Return whether the user has the requested canonical role."""
        name = role.role_name if isinstance(role, Role) else role
        name = _ROLE_ALIASES.get(name, name) if isinstance(name, str) else name
        return self.role.role_name == name

    hasRole = has_role

    def add_session(self, session: UserSession) -> None:
        if self.user_id is None:
            raise ValueError("user must be persisted before sessions can be associated")
        if session.user_id != self.user_id:
            raise ValueError("session belongs to a different user")
        if any(
            existing is session
            or (session.session_id is not None and existing.session_id == session.session_id)
            for existing in self.sessions
        ):
            raise ValueError("session is already associated with this user")
        self.sessions.append(session)

    def to_dict(self) -> dict:
        """Safe public representation; omits password hash and session data."""
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role.to_dict(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass(slots=True)
class UserSession:
    """Persisted session metadata; stores a SHA-256 token digest only."""

    session_id: int | None
    user_id: int
    token_hash: str = field(repr=False)
    expires_at: datetime
    created_at: datetime | None = None
    revoked_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.session_id is not None and (
            not isinstance(self.session_id, int) or isinstance(self.session_id, bool) or self.session_id <= 0
        ):
            raise ValueError("session_id must be a positive integer when provided")
        if not isinstance(self.user_id, int) or isinstance(self.user_id, bool) or self.user_id <= 0:
            raise ValueError("user_id must be a positive integer")
        if not isinstance(self.token_hash, str) or not _TOKEN_HASH_RE.fullmatch(self.token_hash):
            raise ValueError("token_hash must be a 64-character hexadecimal digest")
        if not isinstance(self.expires_at, datetime):
            raise ValueError("expires_at must be a datetime")
        if self.created_at is not None and not isinstance(self.created_at, datetime):
            raise ValueError("created_at must be a datetime when provided")
        if self.revoked_at is not None and not isinstance(self.revoked_at, datetime):
            raise ValueError("revoked_at must be a datetime or None")

        _require_matching_timezone_awareness(self.created_at, self.expires_at, self.revoked_at)
        # MySQL supplies created_at for a new row. Before insertion, the
        # current time is the closest validation point for its CHECK constraint.
        comparison_created_at = self.created_at
        if comparison_created_at is None:
            if self.revoked_at is not None:
                raise ValueError("created_at is required to validate revoked_at")
            comparison_created_at = datetime.now(self.expires_at.tzinfo)
        if self.expires_at <= comparison_created_at:
            raise ValueError("expires_at must be later than created_at")
        if self.revoked_at is not None and self.revoked_at < comparison_created_at:
            raise ValueError("revoked_at cannot be earlier than created_at")

    @classmethod
    def from_record(cls, row: dict) -> UserSession:
        return cls(
            session_id=row["session_id"], user_id=row["user_id"], token_hash=row["token_hash"],
            created_at=row.get("created_at"), expires_at=row["expires_at"],
            revoked_at=row.get("revoked_at"),
        )

    @staticmethod
    def digest_token(token: str) -> str:
        if not isinstance(token, str) or not token:
            raise ValueError("token is required")
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @classmethod
    def create(cls, user_id: int, token: str, expires_at: datetime) -> UserSession:
        return cls(None, user_id, cls.digest_token(token), expires_at)

    @property
    def is_active(self) -> bool:
        if self.revoked_at is not None:
            return False
        try:
            now = datetime.now(self.expires_at.tzinfo)
            return self.expires_at > now
        except (TypeError, ValueError):
            # A mutated or malformed datetime should fail closed rather than
            # make session inspection raise during request handling.
            return False

    def to_dict(self) -> dict:
        """Safe public representation; never includes token credentials."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "revoked_at": self.revoked_at,
        }
