"""Unit tests for Increment 1 domain models (standard-library unittest)."""

import hashlib
import unittest
from datetime import datetime, timedelta, timezone

from models import Role, User, UserSession, verify_password


class RoleTests(unittest.TestCase):
    def test_role_ids_and_names_follow_schema_constraints(self):
        for role_id in (0, -1, True, False):
            with self.subTest(role_id=role_id), self.assertRaises(ValueError):
                Role(role_id, "Volunteer")
        for role_id, role_name in enumerate(("Administrator", "Event Organizer", "Volunteer"), start=1):
            with self.subTest(role_name=role_name):
                self.assertEqual(Role(role_id, role_name).role_name, role_name)
        with self.assertRaises(ValueError):
            Role(4, "Owner")

    def test_record_conversion(self):
        role = Role(1, "Volunteer")
        self.assertEqual(Role.from_record(role.to_dict()), role)


class UserTests(unittest.TestCase):
    def setUp(self):
        self.role = Role(3, "Volunteer")

    def test_user_ids_accept_none_or_positive_int_and_reject_booleans(self):
        self.assertIsNone(User.create("A", "a@example.com", "secret", self.role).user_id)
        for user_id in (0, -1, True, False):
            with self.subTest(user_id=user_id), self.assertRaises(ValueError):
                User(user_id, "A", "a@example.com", "hash", self.role)
        self.assertEqual(User(1, "A", "a@example.com", "hash", self.role).user_id, 1)

    def test_name_email_required_and_length_constraints(self):
        with self.assertRaises(ValueError):
            User.create("  ", "a@example.com", "secret", self.role)
        with self.assertRaises(ValueError):
            User.create("x" * 151, "a@example.com", "secret", self.role)
        self.assertEqual(len(User.create("x" * 150, "a@example.com", "secret", self.role).full_name), 150)
        for email in ("", "@example.com", "name@", "missing-at.example.com"):
            with self.subTest(email=email), self.assertRaises(ValueError):
                User.create("Name", email, "secret", self.role)
        max_email = "a" * 242 + "@example.com"
        self.assertEqual(len(User.create("Name", max_email, "secret", self.role).email), 254)
        with self.assertRaises(ValueError):
            User.create("Name", "a" * 243 + "@example.com", "secret", self.role)

    def test_password_is_salted_and_verified(self):
        first = User.create("A", "a@example.com", "secret", self.role)
        second = User.create("B", "b@example.com", "secret", self.role)
        self.assertNotEqual(first.password_hash, "secret")
        self.assertNotEqual(first.password_hash, second.password_hash)
        self.assertLessEqual(len(first.password_hash), 255)
        self.assertTrue(first.verify_password("secret"))
        self.assertFalse(first.verify_password("wrong"))

    def test_malformed_password_hashes_and_inputs_fail_safely(self):
        malformed_hashes = (
            "", "scrypt$bad$hash", "scrypt$$", None, 42,
            f"scrypt${'00' * 16}${'00' * 63}",
        )
        for password_hash in malformed_hashes:
            with self.subTest(password_hash=password_hash):
                self.assertFalse(verify_password("secret", password_hash))
        self.assertFalse(verify_password(None, "scrypt$" + "00" * 16 + "$" + "00" * 64))

    def test_role_required_and_sensitive_values_hidden(self):
        user = User.create("A User", "a@example.com", "plain-secret", self.role)
        self.assertNotIn("password_hash", user.to_dict())
        self.assertNotIn(user.password_hash, repr(user))
        self.assertNotIn(user.password_hash, str(user.to_dict()))
        self.assertNotIn("plain-secret", repr(user))
        with self.assertRaises(ValueError):
            User(1, "A", "a@example.com", "hash", None)

    def test_record_conversion_and_user_sessions_relationship(self):
        now = datetime.now()
        row = {
            "user_id": 8, "full_name": "A User", "email": "a@example.com",
            "password_hash": "stored-hash", "created_at": now, "updated_at": now,
        }
        user = User.from_record(row, self.role)
        session = UserSession(2, 8, hashlib.sha256(b"token").hexdigest(), now + timedelta(hours=1), now)
        user.add_session(session)
        self.assertEqual(user.sessions, [session])
        other_user_session = UserSession(3, 9, hashlib.sha256(b"other").hexdigest(),
                                         now + timedelta(hours=1), now)
        with self.assertRaises(ValueError):
            user.add_session(other_user_session)

    def test_user_timestamp_values_must_be_datetime_or_none(self):
        now = datetime.now()
        self.assertIsNone(User(1, "A", "a@example.com", "hash", self.role).created_at)
        self.assertEqual(User(1, "A", "a@example.com", "hash", self.role, now, now).created_at, now)
        for field, values in (("created_at", ("not a datetime", 123)),
                              ("updated_at", ("not a datetime", 123))):
            for value in values:
                kwargs = {field: value}
                with self.subTest(field=field, value=value), self.assertRaisesRegex(ValueError, field):
                    User(1, "A", "a@example.com", "hash", self.role, **kwargs)

    def test_user_timestamps_require_matching_timezone_awareness(self):
        naive_created = datetime.now()
        naive_updated = datetime.now()
        aware_created = datetime.now(timezone.utc)
        aware_updated = datetime.now(timezone.utc)

        self.assertEqual(User(1, "A", "a@example.com", "hash", self.role,
                              naive_created, naive_updated).updated_at, naive_updated)
        self.assertEqual(User(1, "A", "a@example.com", "hash", self.role,
                              aware_created, aware_updated).updated_at, aware_updated)
        with self.assertRaisesRegex(ValueError, "timezone"):
            User(1, "A", "a@example.com", "hash", self.role, naive_created, aware_updated)

    def test_add_session_allows_distinct_unsaved_sessions_and_checks_ids_and_ownership(self):
        user = User.from_record({
            "user_id": 8, "full_name": "A User", "email": "a@example.com",
            "password_hash": "stored-hash",
        }, self.role)
        expiry = datetime.now() + timedelta(hours=1)

        first_new = UserSession.create(8, "first-token", expiry)
        second_new = UserSession.create(8, "second-token", expiry)
        user.add_session(first_new)
        user.add_session(second_new)
        self.assertEqual(user.sessions, [first_new, second_new])

        persisted = UserSession(12, 8, hashlib.sha256(b"persisted-a").hexdigest(), expiry)
        duplicate_id = UserSession(12, 8, hashlib.sha256(b"persisted-b").hexdigest(), expiry)
        user.add_session(persisted)
        with self.assertRaisesRegex(ValueError, "already associated"):
            user.add_session(duplicate_id)

        foreign = UserSession.create(9, "foreign-token", expiry)
        with self.assertRaisesRegex(ValueError, "different user"):
            user.add_session(foreign)

        unsaved_user = User.create("New", "new@example.com", "secret", self.role)
        with self.assertRaisesRegex(ValueError, "persisted"):
            unsaved_user.add_session(UserSession.create(1, "not-yet", expiry))


class UserSessionTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime.now()
        self.digest = hashlib.sha256(b"token").hexdigest()

    def test_ids_require_positive_non_boolean_integers(self):
        for session_id in (0, -1, True, False):
            with self.subTest(session_id=session_id), self.assertRaises(ValueError):
                UserSession(session_id, 4, self.digest, self.now + timedelta(hours=1))
        for user_id in (0, -1, True, False):
            with self.subTest(user_id=user_id), self.assertRaises(ValueError):
                UserSession(None, user_id, self.digest, self.now + timedelta(hours=1))
        self.assertIsNone(UserSession(None, 4, self.digest, self.now + timedelta(hours=1)).session_id)

    def test_token_hash_is_exactly_64_hex_characters(self):
        for token_hash in ("a" * 63, "a" * 65, "g" * 64, "raw-token", None):
            with self.subTest(token_hash=token_hash), self.assertRaises(ValueError):
                UserSession(None, 4, token_hash, self.now + timedelta(hours=1))

    def test_expiration_and_revocation_constraints(self):
        with self.assertRaises(ValueError):
            UserSession(1, 4, self.digest, self.now, self.now)
        with self.assertRaises(ValueError):
            UserSession(1, 4, self.digest, self.now + timedelta(hours=1), self.now,
                        self.now - timedelta(microseconds=1))
        valid = UserSession(1, 4, self.digest, self.now + timedelta(hours=1), self.now, self.now)
        self.assertEqual(valid.revoked_at, self.now)

    def test_missing_creation_time_does_not_skip_available_validation(self):
        with self.assertRaises(ValueError):
            UserSession(None, 4, self.digest, self.now - timedelta(seconds=1))
        with self.assertRaises(ValueError):
            UserSession(None, 4, self.digest, self.now + timedelta(hours=1), revoked_at=self.now)
        self.assertIsNone(UserSession(None, 4, self.digest, self.now + timedelta(hours=1)).created_at)

    def test_mixed_aware_and_naive_datetimes_are_rejected(self):
        aware = datetime.now(timezone.utc)
        naive = datetime.now()
        cases = (
            (aware + timedelta(hours=1), naive, None),
            (naive + timedelta(hours=1), aware, None),
            (naive + timedelta(hours=1), naive, aware),
        )
        for expires_at, created_at, revoked_at in cases:
            with self.subTest(created_at=created_at, revoked_at=revoked_at), self.assertRaises(ValueError):
                UserSession(1, 4, self.digest, expires_at, created_at, revoked_at)

    def test_active_expired_and_revoked_states(self):
        active = UserSession.create(4, "active-token", self.now + timedelta(hours=1))
        expired = UserSession(1, 4, self.digest, self.now - timedelta(seconds=1),
                              self.now - timedelta(hours=1))
        revoked = UserSession(2, 4, self.digest, self.now + timedelta(hours=1), self.now, self.now)
        self.assertTrue(active.is_active)
        self.assertFalse(expired.is_active)
        self.assertFalse(revoked.is_active)

    def test_consistent_aware_datetimes_and_active_check(self):
        now = datetime.now(timezone.utc)
        session = UserSession(1, 4, self.digest, now + timedelta(hours=1), now)
        self.assertTrue(session.is_active)

    def test_token_digest_and_safe_representation(self):
        token = "opaque-secret-token"
        session = UserSession.create(4, token, self.now + timedelta(hours=1))
        self.assertEqual(session.token_hash, hashlib.sha256(token.encode()).hexdigest())
        self.assertNotIn(token, repr(session))
        self.assertNotIn(session.token_hash, repr(session))
        self.assertNotIn("token_hash", session.to_dict())
        self.assertNotIn(token, str(session.to_dict()))
        self.assertNotIn(session.token_hash, str(session.to_dict()))

    def test_record_conversion(self):
        row = {
            "session_id": 1, "user_id": 4, "token_hash": self.digest,
            "created_at": self.now, "expires_at": self.now + timedelta(hours=1), "revoked_at": None,
        }
        self.assertEqual(UserSession.from_record(row).session_id, 1)


if __name__ == "__main__":
    unittest.main()
