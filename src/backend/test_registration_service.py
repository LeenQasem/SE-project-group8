"""Unit tests for public registration using a small DB-API test double."""

import unittest

from models import verify_password
from registration_service import (
    DefaultRoleMissing,
    EmailAlreadyRegistered,
    InvalidRegistrationData,
    RegistrationDatabaseError,
    RegistrationService,
)


class DuplicateKeyError(Exception):
    def __init__(self):
        super().__init__(1062, "Duplicate entry for key 'uq_users_email'")


class FakeConnection:
    def __init__(self, volunteer=True, existing_email=False, fail_on=None):
        self.volunteer = volunteer
        self.existing_email = existing_email
        self.fail_on = fail_on
        self.rows = {}
        self.last_user_id = 40
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
        self.lastrowid = None
        self.result = None
        self.executed = []
        self.closed = False

    def execute(self, sql, params):
        self.executed.append((sql, params))
        if self.connection.fail_on == "database":
            raise OSError("private database detail")
        if self.connection.fail_on == "duplicate_insert" and sql.startswith("INSERT"):
            raise DuplicateKeyError()
        if sql.startswith("SELECT role_id"):
            self.result = (3, "Volunteer") if self.connection.volunteer else None
        elif sql.startswith("SELECT user_id FROM users"):
            self.result = (2,) if self.connection.existing_email else None
        elif sql.startswith("INSERT INTO users"):
            self.connection.last_user_id += 1
            self.lastrowid = self.connection.last_user_id
            full_name, email, password_hash, role_id = params
            self.connection.rows[self.lastrowid] = {
                "user_id": self.lastrowid,
                "full_name": full_name,
                "email": email,
                "password_hash": password_hash,
                "role_id": role_id,
                "created_at": None,
                "updated_at": None,
            }
            self.result = None
        elif sql.startswith("SELECT user_id, full_name"):
            self.result = self.connection.rows.get(params[0])
        else:
            raise AssertionError(f"unexpected SQL: {sql}")

    def fetchone(self):
        result, self.result = self.result, None
        return result

    def close(self):
        self.closed = True


class RegistrationServiceTests(unittest.TestCase):
    def service(self, **kwargs):
        connection = FakeConnection(**kwargs)
        return RegistrationService(connection), connection

    def test_success_assigns_volunteer_hashes_password_and_returns_safe_user(self):
        service, connection = self.service()
        result = service.register("  Alex Example ", "ALEX@example.com", "long-enough-password")

        self.assertEqual(result["user_id"], 41)
        self.assertEqual(result["full_name"], "Alex Example")
        self.assertEqual(result["email"], "alex@example.com")
        self.assertEqual(result["role"], {"role_id": 3, "role_name": "Volunteer"})
        self.assertNotIn("password_hash", result)
        self.assertNotIn("password", result)
        stored_hash = connection.rows[41]["password_hash"]
        self.assertNotEqual(stored_hash, "long-enough-password")
        self.assertTrue(verify_password("long-enough-password", stored_hash))
        self.assertEqual(connection.commits, 1)
        self.assertEqual(connection.cursor_instance.executed[0][1], ("Volunteer",))
        self.assertEqual(connection.cursor_instance.executed[2][1][3], 3)

    def test_invalid_email_missing_fields_and_invalid_password_are_rejected(self):
        for fields in (
            {"full_name": "Alex", "email": "bad-email", "password": "secret"},
            {"full_name": "Alex", "email": "alex@example.com", "password": ""},
            {"full_name": "Alex", "email": "alex@example.com"},
            {},
        ):
            service, connection = self.service()
            with self.subTest(fields=fields), self.assertRaises(InvalidRegistrationData):
                service.register(**fields)
            self.assertEqual(connection.cursor_instance, None)

    def test_duplicate_email_is_rejected_before_insert(self):
        service, connection = self.service(existing_email=True)
        with self.assertRaises(EmailAlreadyRegistered):
            service.register("Alex", "alex@example.com", "secret")
        self.assertFalse(any(sql.startswith("INSERT") for sql, _ in connection.cursor_instance.executed))
        self.assertEqual(connection.rollbacks, 1)

    def test_concurrent_duplicate_insert_is_mapped_to_safe_error(self):
        service, connection = self.service(fail_on="duplicate_insert")
        with self.assertRaises(EmailAlreadyRegistered):
            service.register("Alex", "alex@example.com", "secret")
        self.assertEqual(connection.rollbacks, 1)

    def test_missing_volunteer_role_fails_safely(self):
        service, connection = self.service(volunteer=False)
        with self.assertRaises(DefaultRoleMissing):
            service.register("Alex", "alex@example.com", "secret")
        self.assertEqual(connection.rollbacks, 1)

    def test_database_failure_is_wrapped_without_leaking_internal_details(self):
        service, connection = self.service(fail_on="database")
        with self.assertRaises(RegistrationDatabaseError) as raised:
            service.register("Alex", "alex@example.com", "secret")
        self.assertNotIn("private database detail", str(raised.exception))
        self.assertEqual(connection.rollbacks, 1)

    def test_role_cannot_be_supplied_by_public_registration(self):
        service, connection = self.service()
        with self.assertRaises(InvalidRegistrationData):
            service.register("Alex", "alex@example.com", "secret", role="Administrator")
        self.assertIsNone(connection.cursor_instance)


if __name__ == "__main__":
    unittest.main()
