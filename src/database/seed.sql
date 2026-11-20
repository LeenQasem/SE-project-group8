-- Idempotent reference data for the three roles defined in the Increment 1 ERD.
INSERT INTO `Role` (role_name)
VALUES ('Administrator'), ('Event Organizer'), ('Volunteer')
ON DUPLICATE KEY UPDATE role_name = VALUES(role_name);
