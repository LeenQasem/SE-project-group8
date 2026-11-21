"""HTTP-level WSGI tests for all Increment 1 API routes."""

import io
import json
import unittest

from app import create_app
from rbac import AuthorizationError
from user_management_service import UnauthorizedUserManagement


class FakeAuth:
    def register(self, name, email, password):
        if not name or not email or not password:
            raise ValueError("registration fields are required")
        return {"user_id": 3, "full_name": name, "email": email, "role": {"role_name": "Volunteer"}}

    def login(self, email, password):
        if not email or not password:
            raise ValueError("login fields are required")
        if password != "secret":
            from login_service import InvalidCredentials
            raise InvalidCredentials("email or password is incorrect")
        return {"user": {"user_id": 3, "full_name": "A", "role": {"role_name": "Volunteer"}}, "access_token": "user-token", "expires_at": "2030-01-01T00:00:00"}

    def logout(self, token):
        if token != "admin-token":
            raise AuthorizationError("authentication is required")


class FakeAdmin:
    def view_users(self, token):
        if not token:
            raise AuthorizationError("authentication is required")
        if token != "admin-token":
            raise UnauthorizedUserManagement("administrator access is required")
        return [{"user_id": 3, "full_name": "A", "email": "a@example.com", "role": {"role_name": "Volunteer"}}]

    def assign_role(self, token, user_id, role):
        if not token:
            raise AuthorizationError("authentication is required")
        if token != "admin-token":
            raise UnauthorizedUserManagement("administrator access is required")
        if not isinstance(user_id, int) or not role:
            raise ValueError("user_id and role are required")
        return {"user_id": user_id, "role": {"role_name": role}}


class ApiRouteTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(FakeAuth(), FakeAdmin())

    def request(self, method, path, body=None, token=None):
        raw = json.dumps(body).encode() if body is not None else b""
        environ = {"REQUEST_METHOD": method, "PATH_INFO": path, "CONTENT_LENGTH": str(len(raw)),
                   "wsgi.input": io.BytesIO(raw), "CONTENT_TYPE": "application/json"}
        if token:
            environ["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        state = {}
        result = b"".join(self.app(environ, lambda status, headers: state.update(status=status, headers=headers)))
        state["body"] = result
        return state

    def test_root_serves_demo_page(self):
        result = self.request("GET", "/")
        self.assertTrue(result["status"].startswith("200"))
        self.assertIn(b"Volunteer Management System", result["body"])

    def test_register_login_logout_and_role_assignment_success(self):
        registered = self.request("POST", "/api/auth/register", {"name": "A", "email": "a@example.com", "password": "secret"})
        self.assertTrue(registered["status"].startswith("201"))
        logged_in = self.request("POST", "/api/auth/login", {"email": "a@example.com", "password": "secret"})
        self.assertTrue(logged_in["status"].startswith("200"))
        self.assertNotIn(b"password_hash", logged_in["body"])
        self.assertTrue(self.request("POST", "/api/auth/logout", {}, "admin-token")["status"].startswith("200"))
        self.assertTrue(self.request("PATCH", "/api/admin/users/3/role", {"role": "ADMINISTRATOR"}, "admin-token")["status"].startswith("200"))
        self.assertTrue(self.request("POST", "/api/admin/users/role", {"user_id": 3, "role": "VOLUNTEER"}, "admin-token")["status"].startswith("200"))

    def test_admin_list_authorization_and_success(self):
        self.assertTrue(self.request("GET", "/api/admin/users")["status"].startswith("401"))
        self.assertTrue(self.request("GET", "/api/admin/users", token="user-token")["status"].startswith("403"))
        result = self.request("GET", "/api/admin/users", token="admin-token")
        self.assertTrue(result["status"].startswith("200"))
        self.assertIn(b"Volunteer", result["body"])

    def test_validation_and_authentication_errors(self):
        self.assertTrue(self.request("POST", "/api/auth/register", {})["status"].startswith("400"))
        self.assertTrue(self.request("POST", "/api/auth/login", {})["status"].startswith("400"))
        self.assertTrue(self.request("POST", "/api/auth/login", {"email": "a@example.com", "password": "bad"})["status"].startswith("401"))
        self.assertTrue(self.request("POST", "/api/auth/logout", {})["status"].startswith("401"))
        self.assertTrue(self.request("PATCH", "/api/admin/users/3/role", {"role": "VOLUNTEER"})["status"].startswith("401"))
        self.assertTrue(self.request("PATCH", "/api/admin/users/3/role", {"role": "VOLUNTEER"}, "user-token")["status"].startswith("403"))

    def test_malformed_json_and_unknown_route(self):
        environ = {"REQUEST_METHOD": "POST", "PATH_INFO": "/api/auth/login", "CONTENT_LENGTH": "1", "wsgi.input": io.BytesIO(b"{" )}
        state = {}
        b"".join(self.app(environ, lambda status, headers: state.update(status=status)))
        self.assertTrue(state["status"].startswith("400"))
        self.assertTrue(self.request("GET", "/not-found")["status"].startswith("404"))


if __name__ == "__main__":
    unittest.main()
