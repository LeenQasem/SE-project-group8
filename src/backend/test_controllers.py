"""Controller unit tests for the Increment 1 class diagram contracts."""

import unittest
from unittest.mock import Mock

from controllers import AdminUserController, AuthController
from models import User
from rbac import AuthorizationError


class ControllerTests(unittest.TestCase):
    def test_auth_controller_delegates_and_returns_safe_service_data(self):
        registration, login = Mock(), Mock()
        registration.register.return_value = {"user_id": 4, "full_name": "A", "password_hash": "private", "role": {"role_name": "Volunteer"}}
        login.login.return_value = {"user": {"user_id": 4, "token_hash": "private"}, "access_token": "opaque", "expires_at": "later"}
        controller = AuthController(registration, login)
        registered = controller.register("A", "a@example.com", "secret")
        self.assertNotIn("password_hash", registered)
        registration.register.assert_called_once_with(full_name="A", email="a@example.com", password="secret")
        logged_in = controller.login("a@example.com", "secret")
        self.assertNotIn("token_hash", logged_in["user"])
        login.login.assert_called_once_with(email="a@example.com", password="secret")
        self.assertNotIn("password_hash", repr(controller.login("a@example.com", "secret")))

    def test_admin_controller_authenticates_token_then_delegates(self):
        login, management = Mock(), Mock()
        admin = Mock(spec=User)
        login.authenticate_token.return_value = admin
        controller = AdminUserController(login, management)
        controller.view_users("token")
        management.view_users.assert_called_once_with(admin)
        controller.assign_role("token", 9, "VOLUNTEER")
        management.assign_role.assert_called_once_with(admin, 9, "VOLUNTEER")

    def test_admin_controller_rejects_absent_or_non_admin_user(self):
        login, management = Mock(), Mock()
        login.authenticate_token.return_value = None
        controller = AdminUserController(login, management)
        with self.assertRaises(AuthorizationError):
            controller.view_users("bad")
        management.view_users.assert_not_called()


if __name__ == "__main__":
    unittest.main()
