-- Increment 1 data-access examples. Bind values as parameters in the backend;
-- never concatenate user input into SQL. Hash passwords in the application
-- using a strong salted one-way algorithm before inserting/updating.

-- Public registration: role is fixed to Volunteer by the registration flow.
INSERT INTO `User` (full_name, email, password_hash, role_id)
SELECT ?, ?, ?, role_id
FROM `Role`
WHERE role_name = 'Volunteer';

-- Find a login record by email. The backend verifies the supplied password
-- against password_hash; this query does not authenticate a user by itself.
SELECT user_id, full_name, email, password_hash, role_id
FROM `User`
WHERE email = ?;

-- Get an account and its role for role-aware authorization.
SELECT u.user_id, u.full_name, u.email, r.role_name
FROM `User` AS u
JOIN `Role` AS r ON r.role_id = u.role_id
WHERE u.user_id = ?;

-- Administrator account management: list users, optionally ordered by name.
SELECT u.user_id, u.full_name, u.email, r.role_name
FROM `User` AS u
JOIN `Role` AS r ON r.role_id = u.role_id
ORDER BY u.full_name, u.user_id;

-- Update profile fields. Check affected-row count in the application.
UPDATE `User`
SET full_name = ?, email = ?
WHERE user_id = ?;

-- Administrator changes a role using one of the seeded/allowed role names.
UPDATE `User` AS u
JOIN `Role` AS r ON r.role_name = ?
SET u.role_id = r.role_id
WHERE u.user_id = ?;

-- Replace a password only with a newly computed hash.
UPDATE `User`
SET password_hash = ?
WHERE user_id = ?;

-- Delete an account when permitted by application policy. RESTRICT prevents
-- deleting a role still referenced by users.
DELETE FROM `User` WHERE user_id = ?;
