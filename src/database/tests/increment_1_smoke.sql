-- Run only against a disposable Increment 1 test database after applying
-- schema.sql and seed.sql. These assertions do not create or delete data.
DELIMITER //
CREATE PROCEDURE assert_increment_1_schema()
BEGIN
    DECLARE role_count INT DEFAULT 0;
    DECLARE user_table_count INT DEFAULT 0;
    DECLARE role_table_count INT DEFAULT 0;

    SELECT COUNT(*) INTO role_count FROM `Role`;
    IF role_count <> 3 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Expected exactly three seeded roles';
    END IF;

    SELECT COUNT(*) INTO user_table_count
    FROM information_schema.tables
    WHERE table_schema = DATABASE() AND table_name = 'User';
    SELECT COUNT(*) INTO role_table_count
    FROM information_schema.tables
    WHERE table_schema = DATABASE() AND table_name = 'Role';
    IF user_table_count <> 1 OR role_table_count <> 1 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Increment 1 tables are missing';
    END IF;
END//
DELIMITER ;

CALL assert_increment_1_schema();
DROP PROCEDURE assert_increment_1_schema;

-- Manual negative checks in the disposable test database:
-- 1. Insert a User with NULL full_name/email/password_hash/role_id: must fail.
-- 2. Insert duplicate email values: second insert must fail.
-- 3. Insert a User with an unknown role_id: must fail (foreign key).
-- 4. Insert an unknown role_name: must fail (CHECK constraint, MySQL 8.0.16+).
-- 5. Delete a Role referenced by a User: must fail (foreign key RESTRICT).
-- 6. Re-run schema.sql and seed.sql: no duplicate roles or errors.
