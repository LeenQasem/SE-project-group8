"""Tests for authenticated role checks."""

import unittest

from models import Role, User
from rbac import (AuthorizationError, UserRole, authenticate_and_require_admin,
                  require_admin, require_role)


class RBACTests(unittest.TestCase):
    def user(self, role_id, name):
        return User(1, "Test User", "test@example.com", "hash", Role(role_id, name))

    def test_user_role_checks_cover_all_supported_roles(self):
        roles = ((1, "Administrator", UserRole.ADMINISTRATOR),
                 (2, "Event Organizer", UserRole.EVENT_ORGANIZER),
                 (3, "Volunteer", UserRole.VOLUNTEER))
        for role_id, name, expected in roles:
            with self.subTest(role=name):
                user = self.user(role_id, name)
                self.assertTrue(user.has_role(expected))
                self.assertTrue(user.hasRole(name))
                self.assertIs(require_role(user, expected), user)

    def test_admin_guard_rejects_unauthenticated_and_non_admin_users(self):
        for user in (None, self.user(2, "Event Organizer"), self.user(3, "Volunteer")):
            with self.subTest(user=user), self.assertRaises(AuthorizationError):
                require_admin(user)
        admin = self.user(1, "Administrator")
        self.assertIs(require_admin(admin), admin)

    def test_admin_token_check_resolves_current_principal_through_login_service(self):
        admin = self.user(1, "Administrator")

        class LoginStub:
            def authenticate_token(self, token):
                return admin if token == "valid" else None

        self.assertIs(authenticate_and_require_admin(LoginStub(), "valid"), admin)
        for token in (None, "invalid"):
            with self.subTest(token=token), self.assertRaises(AuthorizationError):
                authenticate_and_require_admin(LoginStub(), token)


if __name__ == "__main__":
    unittest.main()
