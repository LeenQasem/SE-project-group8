-- Increment 1 user management operations. Application values use ? placeholders.
-- The Python backend must hash passwords with a strong salted one-way
-- password-hashing algorithm before INSERT/UPDATE. Never pass plaintext here.

-- USER REGISTRATION
-- Roles are seeded by seed.sql. The backend must not accept a role from the
-- public registration request. The scalar subquery yields NULL if the required
-- Volunteer role is missing; users.role_id is NOT NULL, so MySQL raises an
-- error instead of reporting a successful zero-row INSERT.

INSERT INTO users (full_name, email, password_hash, role_id)
VALUES (?, ?, ?, (SELECT role_id FROM roles WHERE role_name = 'Volunteer'));

-- AUTHENTICATION LOOKUP
-- Find a user by email for backend password-hash verification.
SELECT user_id, full_name, email, password_hash, role_id, created_at, updated_at
FROM users
WHERE email = ?;

-- USER MANAGEMENT (administrator authorization is enforced by the backend)
SELECT u.user_id, u.full_name, u.email, r.role_name, u.created_at, u.updated_at
FROM users AS u
JOIN roles AS r ON r.role_id = u.role_id
ORDER BY u.user_id;

-- Retrieve one account by its key.
SELECT u.user_id, u.full_name, u.email, r.role_name, u.created_at, u.updated_at
FROM users AS u
JOIN roles AS r ON r.role_id = u.role_id
WHERE u.user_id = ?;

-- Update permitted profile fields. Role assignment is a separate admin action.
UPDATE users SET full_name = ?, email = ? WHERE user_id = ?;

-- Assign a role only after backend administrator authorization. Run these
-- statements in one transaction: verify the account exists, resolve the
-- allowlisted role, then update. Checking existence separately avoids treating
-- an unchanged role (0 changed rows) as a missing account.
SELECT user_id FROM users WHERE user_id = ? FOR UPDATE;
SELECT role_id FROM roles WHERE role_name = ?;
UPDATE users SET role_id = ? WHERE user_id = ?;

-- Delete an account when permitted. Related persisted sessions cascade-delete.
DELETE FROM users WHERE user_id = ?;

-- Persist a session using the application-selected 64-character token digest.
-- Store only the digest, never the bearer token itself. The ERD does not
-- specify a digest algorithm or encoding; agree on these at backend integration.
INSERT INTO user_sessions (user_id, token_hash, expires_at)
VALUES (?, ?, ?);

-- Validate a session at request time.
SELECT s.session_id, u.user_id, u.full_name, u.email, r.role_name
FROM user_sessions AS s
JOIN users AS u ON u.user_id = s.user_id
JOIN roles AS r ON r.role_id = u.role_id
WHERE s.token_hash = ?
  AND s.revoked_at IS NULL
  AND s.expires_at > CURRENT_TIMESTAMP;

-- Revoke a session on logout; do not physically delete it.
UPDATE user_sessions
SET revoked_at = CURRENT_TIMESTAMP
WHERE token_hash = ? AND revoked_at IS NULL;

-- Clean up expired/revoked session history under an application retention
-- policy. No retention duration is specified by the approved requirements.
DELETE FROM user_sessions
WHERE expires_at <= CURRENT_TIMESTAMP
   OR revoked_at < ?;

-- Future increments (not implemented here): event CRUD/discovery (I2),
-- applications/assignments/attendance/hours (I3), and reports (I4).
