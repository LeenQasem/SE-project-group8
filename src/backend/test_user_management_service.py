"""Unit tests for user profile and administrator management operations."""

import unittest

from user_management_service import (
    EmailAlreadyInUse,
    InvalidUserManagementData,
    UnauthorizedUserManagement,
    UserManagementDatabaseError,
    UserManagementService,
    UserNotFound,
)


class FakeConnection:
    def __init__(self, fail=False):
        self.fail = fail
        self.commits = 0
        self.rollbacks = 0
        self.cursor_instance = None
        self.executed = []

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
        self.row = {
            "user_id": 7, "full_name": "Alex Example", "email": "alex@example.com",
            "password_hash": "scrypt$secret", "role_id": 3, "role_name": "Volunteer",
            "created_at": None, "updated_at": None,
        }
        self.executed = []

    def execute(self, sql, params):
        self.executed.append((sql, params))
        self.connection.executed.append((sql, params))
        if self.connection.fail:
            raise OSError("private database detail")
        if "WHERE u.user_id = ?" in sql:
            self.row = dict(self.row, user_id=params[0]) if params[0] == 7 else None
        elif "ORDER BY u.user_id LIMIT" in sql:
            pass
        elif sql.startswith("SELECT user_id FROM users WHERE email"):
            self.row = (8,) if params[0] == "taken@example.com" else None

    def fetchone(self):
        return self.row

    def fetchall(self):
        return [self.row]

    def close(self):
        pass


class UserManagementServiceTests(unittest.TestCase):
    def service(self, **kwargs):
        connection = FakeConnection(**kwargs)
        return UserManagementService(connection), connection

    def test_get_user_returns_role_and_never_sensitive_fields(self):
        service, _ = self.service()
        result = service.get_user(7, actor_id=1, actor_role="Administrator")
        self.assertEqual(result["role"]["role_name"], "Volunteer")
        self.assertNotIn("password_hash", result)
        self.assertNotIn("sessions", result)

    def test_authenticated_user_can_retrieve_own_profile(self):
        service, _ = self.service()
        self.assertEqual(service.get_my_profile(actor_id=7)["user_id"], 7)

    def test_ordinary_user_cannot_read_another_profile_or_list_users(self):
        service, connection = self.service()
        with self.assertRaises(UnauthorizedUserManagement):
            service.get_user(8, actor_id=7, actor_role="Volunteer")
        with self.assertRaises(UnauthorizedUserManagement):
            service.list_users(actor_id=7, actor_role="Volunteer")
        self.assertIsNone(connection.cursor_instance)

    def test_administrator_can_list_users_with_pagination(self):
        service, connection = self.service()
        users = service.list_users(actor_id=1, actor_role="Administrator", limit=20, offset=10)
        self.assertEqual(users[0]["role"]["role_name"], "Volunteer")
        self.assertEqual(connection.executed[0][1], (20, 10))
        self.assertNotIn("password_hash", users[0])

    def test_self_update_validates_values_and_commits_safe_fields(self):
        service, connection = self.service()
        result = service.update_profile(7, {"full_name": "  Alex New  "}, actor_id=7, actor_role="Volunteer")
        self.assertEqual(result["user_id"], 7)
        update = next(call for call in connection.executed if call[0].startswith("UPDATE"))
        self.assertEqual(update[1], ("Alex New", "alex@example.com", 7))
        self.assertEqual(connection.commits, 1)

    def test_profile_updates_reject_privileged_fields_and_invalid_email(self):
        service, _ = self.service()
        for changes in ({"role": "Administrator"}, {"password_hash": "x"}, {"email": "bad"}):
            with self.subTest(changes=changes), self.assertRaises(InvalidUserManagementData):
                service.update_profile(7, changes, actor_id=7, actor_role="Volunteer")

    def test_email_uniqueness_is_checked_before_update(self):
        service, connection = self.service()
        with self.assertRaises(EmailAlreadyInUse):
            service.update_profile(7, {"email": "taken@example.com"}, actor_id=7, actor_role="Volunteer")
        self.assertEqual(connection.commits, 0)

    def test_missing_user_and_invalid_identifier_are_reported(self):
        service, _ = self.service()
        with self.assertRaises(UserNotFound):
            service.get_user(8, actor_id=1, actor_role="Administrator")
        with self.assertRaises(InvalidUserManagementData):
            service.get_my_profile(actor_id=True)

    def test_database_failures_are_wrapped_without_leaking_details(self):
        service, connection = self.service(fail=True)
        with self.assertRaises(UserManagementDatabaseError) as raised:
            service.get_my_profile(actor_id=7)
        self.assertNotIn("private database detail", str(raised.exception))
        self.assertEqual(connection.rollbacks, 1)


if __name__ == "__main__":
    unittest.main()
