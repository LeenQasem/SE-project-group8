"""Zero-dependency WSGI JSON API for Increment 1.

Create the app with service-backed controllers, then serve it with
``wsgiref.simple_server``. A DB-API connection factory must be supplied by the
deployment because this repository does not select a Python MySQL driver.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
from datetime import date, datetime
from http import HTTPStatus
from pathlib import Path

try:
    from .login_service import InvalidCredentials, InvalidLoginData, LoginDatabaseError, LoginError
    from .registration_service import (DefaultRoleMissing, EmailAlreadyRegistered,
        InvalidRegistrationData, RegistrationDatabaseError, RegistrationError)
    from .rbac import AuthorizationError
    from .user_management_service import (InvalidUserManagementData, UnauthorizedUserManagement,
        UserManagementDatabaseError, UserManagementError, UserNotFound)
except ImportError:  # pragma: no cover
    from login_service import InvalidCredentials, InvalidLoginData, LoginDatabaseError, LoginError
    from registration_service import (DefaultRoleMissing, EmailAlreadyRegistered,
        InvalidRegistrationData, RegistrationDatabaseError, RegistrationError)
    from rbac import AuthorizationError
    from user_management_service import (InvalidUserManagementData, UnauthorizedUserManagement,
        UserManagementDatabaseError, UserManagementError, UserNotFound)


def _json_default(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    raise TypeError(f"unsupported JSON value: {type(value).__name__}")


def create_app(auth_controller, admin_controller, frontend_path=None):
    """Return a WSGI callable suitable for tests and ``wsgiref`` serving."""
    page = Path(frontend_path) if frontend_path else Path(__file__).resolve().parents[1] / "frontend" / "index.html"

    def app(environ, start_response):
        method, path = environ.get("REQUEST_METHOD", "GET").upper(), environ.get("PATH_INFO", "/")
        try:
            if method == "GET" and path == "/":
                body, content_type = page.read_bytes(), "text/html; charset=utf-8"
                return _respond(start_response, HTTPStatus.OK, body, content_type)
            payload = _read_json(environ) if method in {"POST", "PATCH", "PUT"} else {}
            token = _bearer(environ)
            if method == "POST" and path == "/api/auth/register":
                result = auth_controller.register(payload.get("name"), payload.get("email"), payload.get("password"))
                return _respond(start_response, HTTPStatus.CREATED, result)
            if method == "POST" and path == "/api/auth/login":
                return _respond(start_response, HTTPStatus.OK, auth_controller.login(payload.get("email"), payload.get("password")))
            if method == "POST" and path == "/api/auth/logout":
                if not token:
                    return _respond(start_response, HTTPStatus.UNAUTHORIZED, {"error": "authentication is required"})
                auth_controller.logout(token)
                return _respond(start_response, HTTPStatus.OK, {"message": "Logged out"})
            if method == "GET" and path == "/api/admin/users":
                return _respond(start_response, HTTPStatus.OK, {"users": admin_controller.view_users(token)})
            role_match = re.fullmatch(r"/api/admin/users/(\d+)/role", path)
            if method == "PATCH" and role_match:
                result = admin_controller.assign_role(token, int(role_match.group(1)), payload.get("role"))
                return _respond(start_response, HTTPStatus.OK, result)
            if method == "POST" and path == "/api/admin/users/role":
                result = admin_controller.assign_role(token, payload.get("user_id"), payload.get("role"))
                return _respond(start_response, HTTPStatus.OK, result)
            return _respond(start_response, HTTPStatus.NOT_FOUND, {"error": "Route not found"})
        except (ValueError, TypeError, InvalidLoginData, InvalidRegistrationData, InvalidUserManagementData) as error:
            return _respond(start_response, HTTPStatus.BAD_REQUEST, {"error": str(error)})
        except (InvalidCredentials, AuthorizationError, UnauthorizedUserManagement) as error:
            unauthorized = isinstance(error, InvalidCredentials) or "authentication is required" in str(error).lower()
            return _respond(start_response, HTTPStatus.UNAUTHORIZED if unauthorized else HTTPStatus.FORBIDDEN,
                            {"error": str(error)})
        except UserNotFound as error:
            return _respond(start_response, HTTPStatus.NOT_FOUND, {"error": str(error)})
        except (EmailAlreadyRegistered,) as error:
            return _respond(start_response, HTTPStatus.CONFLICT, {"error": str(error)})
        except (RegistrationError, LoginError, UserManagementError, RuntimeError) as error:
            return _respond(start_response, HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(error)})
        except Exception:
            return _respond(start_response, HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "Request could not be completed"})

    return app


def create_app_from_connection(connection, frontend_path=None):
    """Wire the existing services/controllers around an injected DB connection."""
    try:
        from .controllers import AdminUserController, AuthController
        from .login_service import LoginService
        from .registration_service import RegistrationService
        from .user_management_service import UserManagementService
    except ImportError:  # pragma: no cover
        from controllers import AdminUserController, AuthController
        from login_service import LoginService
        from registration_service import RegistrationService
        from user_management_service import UserManagementService
    registration, login = RegistrationService(connection), LoginService(connection)
    auth = AuthController(registration, login, connection)
    admin = AdminUserController(login, UserManagementService(connection))
    return create_app(auth, admin, frontend_path)


def serve(connection, host="127.0.0.1", port=8000):
    """Run the API using a caller-provided DB-API connection."""
    from wsgiref.simple_server import make_server
    application = create_app_from_connection(connection)
    with make_server(host, port, application) as server:
        print(f"Server running at http://{host}:{port}", flush=True)
        server.serve_forever()


def create_local_demo_connection():
    """Initialize an in-memory SQLite database for direct local execution.

    This intentionally small SQLite schema mirrors Increment 1's MySQL schema.
    The local administrator credentials can be overridden with
    ``DEMO_ADMIN_EMAIL`` and ``DEMO_ADMIN_PASSWORD``.
    """
    try:
        from .models import hash_password
    except ImportError:  # pragma: no cover - direct script execution
        from models import hash_password

    sqlite3.register_converter("DATETIME", lambda value: datetime.fromisoformat(value.decode("utf-8")))
    connection = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    connection.row_factory = sqlite3.Row
    connection.executescript("""
        PRAGMA foreign_keys = ON;
        CREATE TABLE roles (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL UNIQUE CHECK (
                role_name IN ('Administrator', 'Event Organizer', 'Volunteer')
            )
        );
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL CHECK (length(trim(full_name)) BETWEEN 1 AND 150),
            email TEXT NOT NULL UNIQUE CHECK (length(trim(email)) BETWEEN 1 AND 254),
            password_hash TEXT NOT NULL CHECK (length(password_hash) > 0),
            role_id INTEGER NOT NULL REFERENCES roles(role_id),
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TRIGGER users_updated_at AFTER UPDATE ON users
        FOR EACH ROW WHEN NEW.updated_at = OLD.updated_at
        BEGIN
            UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE user_id = NEW.user_id;
        END;
        CREATE TABLE user_sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
            token_hash TEXT NOT NULL UNIQUE CHECK (length(token_hash) = 64),
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            expires_at DATETIME NOT NULL,
            revoked_at DATETIME DEFAULT NULL,
            CHECK (expires_at > created_at),
            CHECK (revoked_at IS NULL OR revoked_at >= created_at)
        );
        CREATE INDEX ix_users_role_id ON users(role_id);
        CREATE INDEX ix_user_sessions_user_expiry ON user_sessions(user_id, expires_at);
        CREATE INDEX ix_user_sessions_active_expiry ON user_sessions(expires_at, revoked_at);
    """)
    connection.executemany(
        "INSERT INTO roles (role_id, role_name) VALUES (?, ?)",
        [(1, "Administrator"), (2, "Event Organizer"), (3, "Volunteer")],
    )
    email = os.environ.get("DEMO_ADMIN_EMAIL", "admin@example.com").strip().lower()
    password = os.environ.get("DEMO_ADMIN_PASSWORD", "Admin123!")
    if not email or not password:
        raise ValueError("DEMO_ADMIN_EMAIL and DEMO_ADMIN_PASSWORD must be nonempty")
    connection.execute(
        "INSERT INTO users (full_name, email, password_hash, role_id) VALUES (?, ?, ?, ?)",
        ("Demo Administrator", email, hash_password(password), 1),
    )
    connection.commit()
    return connection


def main():
    """Start a self-contained local demo at 127.0.0.1:8000."""
    serve(create_local_demo_connection(), host="127.0.0.1", port=8000)


def _read_json(environ):
    try:
        length = int(environ.get("CONTENT_LENGTH") or 0)
    except ValueError as error:
        raise ValueError("invalid content length") from error
    if length < 0 or length > 1024 * 1024:
        raise ValueError("request body is too large")
    raw = environ["wsgi.input"].read(length) if length else b"{}"
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("request body must be valid JSON") from error
    if not isinstance(value, dict):
        raise ValueError("JSON body must be an object")
    return value


def _bearer(environ):
    value = environ.get("HTTP_AUTHORIZATION", "")
    if not value:
        return None
    scheme, separator, token = value.partition(" ")
    return token.strip() if separator and scheme.lower() == "bearer" and token.strip() else None


def _respond(start_response, status, data, content_type="application/json; charset=utf-8"):
    body = data if isinstance(data, bytes) else json.dumps(data, default=_json_default).encode("utf-8")
    phrase = status.phrase
    start_response(f"{status.value} {phrase}", [("Content-Type", content_type), ("Content-Length", str(len(body))), ("Cache-Control", "no-store")])
    return [body]


__all__ = ["create_app", "create_app_from_connection", "create_local_demo_connection", "main", "serve"]


if __name__ == "__main__":
    main()
