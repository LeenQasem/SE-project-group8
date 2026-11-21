"""Unit tests for login and persisted sessions using a DB-API test double."""

import unittest

from models import Role, User
from login_service import (
    InvalidCredentials,
    InvalidLoginData,
    LoginDatabaseError,
    LoginService,
    SessionCreationError,
)


class FakeConnection:
    def __init__(self, row=None, fail_lookup=False, fail_session=False):
        role = {"role_id": 3, "role_name": "Volunteer"}
        user = User.create("Alex Example", "alex@example.com", "valid-secret", Role(**role))
        self.row = row if row is not None else {
            "user_id": 7, "full_name": user.full_name, "email": user.email,
            "password_hash": user.password_hash, "role_id": 3,
            "created_at": None, "updated_at": None, "role_name": "Volunteer",
        }
        self.fail_lookup = fail_lookup
        self.fail_session = fail_session
        self.commits = 0
        self.rollbacks = 0
        self.cursor_instance = None

    def cursor(self):
        self.cursor_instance = FakeCursor(self)
        return self.cursor_instance

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1


class FakeCursor:
    def __init__(self, connection):
        self.connection = connection
        self.result = None
        self.executed = []

    def execute(self, sql, params):
        self.executed.append((sql, params))
        if sql.startswith("SELECT"):
            if self.connection.fail_lookup:
                raise OSError("private db error")
            self.result = self.connection.row
        else:
            if self.connection.fail_session:
                raise OSError("private session error")
            self.result = None

    def fetchone(self):
        result, self.result = self.result, None
        return result

    def close(self):
        pass


class LoginServiceTests(unittest.TestCase):
    def service(self, **kwargs):
        connection = FakeConnection(**kwargs)
        return LoginService(connection), connection

    def test_success_returns_user_role_and_opaque_token_only(self):
        service, connection = self.service()
        result = service.login(" ALEX@example.com ", "valid-secret")
        self.assertEqual(result["user"]["user_id"], 7)
        self.assertEqual(result["user"]["role"]["role_name"], "Volunteer")
        self.assertNotIn("password_hash", result["user"])
        self.assertNotIn("valid-secret", repr(result))
        token_hash = connection.cursor_instance.executed[1][1][1]
        self.assertEqual(len(token_hash), 64)
        self.assertNotEqual(token_hash, result["access_token"])
        self.assertEqual(connection.commits, 1)

    def test_missing_and_invalid_inputs_are_rejected_before_database_access(self):
        for email, password in ((None, "x"), ("alex@example.com", None), ("bad", "x")):
            service, connection = self.service()
            with self.subTest(email=email, password=password), self.assertRaises(InvalidLoginData):
                service.login(email, password)
            self.assertIsNone(connection.cursor_instance)

    def test_unknown_email_and_wrong_password_have_same_error(self):
        service, _ = self.service(row=None)
        with self.assertRaises(InvalidCredentials) as unknown:
            service.login("alex@example.com", "wrong")
        service, _ = self.service()
        with self.assertRaises(InvalidCredentials) as wrong:
            service.login("alex@example.com", "wrong")
        self.assertEqual(str(unknown.exception), str(wrong.exception))

    def test_database_and_session_failures_are_safe(self):
        service, connection = self.service(fail_lookup=True)
        with self.assertRaises(LoginDatabaseError) as raised:
            service.login("alex@example.com", "valid-secret")
        self.assertNotIn("private db error", str(raised.exception))
        self.assertEqual(connection.rollbacks, 1)
        service, connection = self.service(fail_session=True)
        with self.assertRaises(SessionCreationError):
            service.login("alex@example.com", "valid-secret")
        self.assertEqual(connection.rollbacks, 1)

    def test_login_does_not_accept_role_override(self):
        service, _ = self.service()
        with self.assertRaises(TypeError):
            service.login("alex@example.com", "valid-secret", role="Administrator")


if __name__ == "__main__":
    unittest.main()
