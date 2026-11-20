-- Increment 1 database integration smoke tests.
-- Run after schema.sql and seed.sql, against a disposable MySQL 8.0.16+
-- database. All test users are rolled back; the procedure is removed on
-- success and is dropped at the start of the next run if an assertion fails.
DELIMITER $$
DROP PROCEDURE IF EXISTS run_increment_1_smoke_tests$$
CREATE PROCEDURE run_increment_1_smoke_tests()
BEGIN
    DECLARE actual_count INT DEFAULT 0;
    DECLARE approved_role_count INT DEFAULT 0;
    DECLARE actual_errno INT DEFAULT 0;
    DECLARE expected_errno INT DEFAULT 0;
    DECLARE volunteer_role_id BIGINT UNSIGNED;
    DECLARE organizer_role_id BIGINT UNSIGNED;
    DECLARE test_user_id BIGINT UNSIGNED;
    DECLARE updated_user_id BIGINT UNSIGNED;
    DECLARE test_email VARCHAR(254);
    DECLARE updated_email VARCHAR(254);
    DECLARE duplicate_pk_email VARCHAR(254);
    DECLARE actual_name VARCHAR(150);
    DECLARE actual_email VARCHAR(254);
    DECLARE actual_hash VARCHAR(255);
    DECLARE actual_role VARCHAR(30);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    -- Required Increment 1 tables and columns. Additional columns are allowed
    -- so later approved increments can extend these tables.
    SELECT COUNT(*) INTO actual_count
    FROM information_schema.tables
    WHERE table_schema = DATABASE()
      AND table_name IN ('Role', 'User')
      AND table_type = 'BASE TABLE';
    IF actual_count <> 2 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Expected Role and User tables';
    END IF;

    SELECT COUNT(*) INTO actual_count
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND ((table_name = 'Role' AND column_name IN ('role_id', 'role_name'))
        OR (table_name = 'User' AND column_name IN
            ('user_id', 'full_name', 'email', 'password_hash', 'role_id')));
    IF actual_count <> 7 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Expected all seven Increment 1 columns';
    END IF;

    -- Verify types for every required Increment 1 column without rejecting
    -- additional columns added by later approved increments.
    SELECT COUNT(*) INTO actual_count
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND ((table_name = 'Role' AND column_name = 'role_id' AND column_type = 'bigint unsigned')
        OR (table_name = 'Role' AND column_name = 'role_name' AND column_type = 'varchar(30)')
        OR (table_name = 'User' AND column_name = 'user_id' AND column_type = 'bigint unsigned')
        OR (table_name = 'User' AND column_name = 'full_name' AND column_type = 'varchar(150)')
        OR (table_name = 'User' AND column_name = 'email' AND column_type = 'varchar(254)')
        OR (table_name = 'User' AND column_name = 'password_hash' AND column_type = 'varchar(255)')
        OR (table_name = 'User' AND column_name = 'role_id' AND column_type = 'bigint unsigned'));
    IF actual_count <> 7 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Increment 1 column types do not match the ERD';
    END IF;

    SELECT COUNT(*) INTO actual_count
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND ((table_name = 'Role' AND column_name IN ('role_id', 'role_name'))
        OR (table_name = 'User' AND column_name IN
            ('user_id', 'full_name', 'email', 'password_hash', 'role_id')))
      AND is_nullable = 'NO';
    IF actual_count <> 7 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'All ERD attributes must be NOT NULL';
    END IF;

    -- PK, unique email/role name, and Role-to-User FK metadata.
    SELECT COUNT(*) INTO actual_count
    FROM information_schema.table_constraints
    WHERE constraint_schema = DATABASE()
      AND table_name IN ('Role', 'User')
      AND constraint_type = 'PRIMARY KEY';
    IF actual_count <> 2 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Expected primary keys on Role and User';
    END IF;

    SELECT COUNT(*) INTO actual_count
    FROM information_schema.key_column_usage
    WHERE constraint_schema = DATABASE()
      AND constraint_name = 'PRIMARY'
      AND ((table_name = 'Role' AND column_name = 'role_id')
        OR (table_name = 'User' AND column_name = 'user_id'));
    IF actual_count <> 2 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Primary keys must use role_id and user_id';
    END IF;

    SELECT COUNT(*) INTO actual_count
    FROM information_schema.key_column_usage
    WHERE constraint_schema = DATABASE()
      AND table_name IN ('Role', 'User')
      AND constraint_name = 'PRIMARY';
    IF actual_count <> 2 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Role and User primary keys must be single-column';
    END IF;

    SELECT COUNT(*) INTO actual_count
    FROM information_schema.statistics AS s
    WHERE s.table_schema = DATABASE()
      AND ((s.table_name = 'User' AND s.index_name = 'uq_user_email'
            AND s.column_name = 'email' AND s.non_unique = 0)
        OR (s.table_name = 'Role' AND s.index_name = 'uq_role_name'
            AND s.column_name = 'role_name' AND s.non_unique = 0))
      AND (SELECT COUNT(*)
           FROM information_schema.statistics AS index_columns
           WHERE index_columns.table_schema = s.table_schema
             AND index_columns.table_name = s.table_name
             AND index_columns.index_name = s.index_name) = 1;
    IF actual_count <> 2 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Expected unique email and role_name constraints';
    END IF;

    SELECT COUNT(*) INTO actual_count
    FROM information_schema.key_column_usage
    WHERE constraint_schema = DATABASE()
      AND table_name = 'User'
      AND column_name = 'role_id'
      AND referenced_table_name = 'Role'
      AND referenced_column_name = 'role_id';
    IF actual_count <> 1 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Expected User.role_id foreign key to Role.role_id';
    END IF;

    SELECT COUNT(*) INTO actual_count
    FROM information_schema.referential_constraints
    WHERE constraint_schema = DATABASE()
      AND constraint_name = 'fk_user_role'
      AND table_name = 'User'
      AND referenced_table_name = 'Role'
      AND delete_rule = 'RESTRICT'
      AND update_rule = 'RESTRICT';
    IF actual_count <> 1 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Role foreign key must RESTRICT update and delete';
    END IF;

    -- Exact seeded role set (no missing or additional roles).
    SELECT COUNT(*) INTO actual_count FROM `Role`;
    SELECT COUNT(*) INTO approved_role_count
    FROM `Role`
    WHERE role_name IN ('Administrator', 'Event Organizer', 'Volunteer');
    IF actual_count <> 3 OR approved_role_count <> 3 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Expected exactly the three approved roles';
    END IF;

    SELECT role_id INTO volunteer_role_id FROM `Role` WHERE role_name = 'Volunteer';
    SELECT role_id INTO organizer_role_id FROM `Role` WHERE role_name = 'Event Organizer';

    -- Positive CRUD and relationship behavior, isolated in a rolled-back transaction.
    START TRANSACTION;
    SET test_email = CONCAT('smoke-', REPLACE(UUID(), '-', ''), '@example.test');
    SET updated_email = CONCAT('updated-', REPLACE(UUID(), '-', ''), '@example.test');
    SET duplicate_pk_email = CONCAT('duplicate-pk-', REPLACE(UUID(), '-', ''), '@example.test');

    INSERT INTO `User` (full_name, email, password_hash, role_id)
    VALUES ('Smoke Test Volunteer', test_email, 'test-only-hash-value', volunteer_role_id);
    SET test_user_id = LAST_INSERT_ID();
    SET updated_user_id = test_user_id;
    IF test_user_id IS NULL OR test_user_id = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User primary key was not generated';
    END IF;

    SELECT u.full_name, u.email, u.password_hash, r.role_name
    INTO actual_name, actual_email, actual_hash, actual_role
    FROM `User` AS u JOIN `Role` AS r ON r.role_id = u.role_id
    WHERE u.user_id = test_user_id;
    IF actual_name <> 'Smoke Test Volunteer' OR actual_email <> test_email
       OR actual_hash <> 'test-only-hash-value' OR actual_role <> 'Volunteer' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User insert or role relationship failed';
    END IF;

    UPDATE `User`
    SET full_name = 'Updated Smoke User', email = updated_email,
        password_hash = 'updated-test-hash-value', role_id = organizer_role_id
    WHERE user_id = test_user_id;
    SELECT u.full_name, u.email, u.password_hash, r.role_name
    INTO actual_name, actual_email, actual_hash, actual_role
    FROM `User` AS u JOIN `Role` AS r ON r.role_id = u.role_id
    WHERE u.user_id = test_user_id;
    IF actual_name <> 'Updated Smoke User' OR actual_email <> updated_email
       OR actual_hash <> 'updated-test-hash-value' OR actual_role <> 'Event Organizer' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User update or role change failed';
    END IF;

    -- Negative tests: each expected database error is caught and asserted.
    SET expected_errno = 1062;
    SET actual_errno = 0;
    BEGIN
        DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            GET DIAGNOSTICS CONDITION 1 actual_errno = MYSQL_ERRNO;
        END;
        INSERT INTO `User` (user_id, full_name, email, password_hash, role_id)
        VALUES (updated_user_id, 'Duplicate PK', duplicate_pk_email, 'test-hash', volunteer_role_id);
    END;
    IF actual_errno <> expected_errno THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Duplicate primary key must raise MySQL error 1062';
    END IF;

    -- A fresh row with a unique PK reaches the email unique constraint.
    SET test_email = CONCAT('unique-', REPLACE(UUID(), '-', ''), '@example.test');
    INSERT INTO `User` (full_name, email, password_hash, role_id)
    VALUES ('Email Constraint Fixture', test_email, 'test-hash', volunteer_role_id);
    SET test_user_id = LAST_INSERT_ID();
    SET expected_errno = 1062;
    SET actual_errno = 0;
    BEGIN
        DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            GET DIAGNOSTICS CONDITION 1 actual_errno = MYSQL_ERRNO;
        END;
        INSERT INTO `User` (full_name, email, password_hash, role_id)
        VALUES ('Duplicate Email', test_email, 'test-hash', volunteer_role_id);
    END;
    IF actual_errno <> expected_errno THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Duplicate email must raise MySQL error 1062';
    END IF;

    -- Required User attributes must reject NULL independently.
    SET expected_errno = 1048;
    SET actual_errno = 0;
    BEGIN
        DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            GET DIAGNOSTICS CONDITION 1 actual_errno = MYSQL_ERRNO;
        END;
        INSERT INTO `User` (full_name, email, password_hash, role_id)
        VALUES (NULL, CONCAT('null-name-', REPLACE(UUID(), '-', ''), '@example.test'),
                'test-hash', volunteer_role_id);
    END;
    IF actual_errno <> expected_errno THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'NULL full_name must raise MySQL error 1048';
    END IF;

    SET expected_errno = 1048;
    SET actual_errno = 0;
    BEGIN
        DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            GET DIAGNOSTICS CONDITION 1 actual_errno = MYSQL_ERRNO;
        END;
        INSERT INTO `User` (full_name, email, password_hash, role_id)
        VALUES ('Null Email', NULL, 'test-hash', volunteer_role_id);
    END;
    IF actual_errno <> expected_errno THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'NULL email must raise MySQL error 1048';
    END IF;

    SET expected_errno = 1048;
    SET actual_errno = 0;
    BEGIN
        DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            GET DIAGNOSTICS CONDITION 1 actual_errno = MYSQL_ERRNO;
        END;
        INSERT INTO `User` (full_name, email, password_hash, role_id)
        VALUES ('Null Hash', CONCAT('null-hash-', REPLACE(UUID(), '-', ''), '@example.test'),
                NULL, volunteer_role_id);
    END;
    IF actual_errno <> expected_errno THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'NULL password_hash must raise MySQL error 1048';
    END IF;

    SET expected_errno = 1048;
    SET actual_errno = 0;
    BEGIN
        DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            GET DIAGNOSTICS CONDITION 1 actual_errno = MYSQL_ERRNO;
        END;
        INSERT INTO `User` (full_name, email, password_hash, role_id)
        VALUES ('Null Role', CONCAT('null-role-', REPLACE(UUID(), '-', ''), '@example.test'),
                'test-hash', NULL);
    END;
    IF actual_errno <> expected_errno THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'NULL role_id must raise MySQL error 1048';
    END IF;

    SET expected_errno = 1452;
    SET actual_errno = 0;
    BEGIN
        DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            GET DIAGNOSTICS CONDITION 1 actual_errno = MYSQL_ERRNO;
        END;
        INSERT INTO `User` (full_name, email, password_hash, role_id)
        VALUES ('Invalid FK', CONCAT('bad-fk-', REPLACE(UUID(), '-', ''), '@example.test'),
                'test-hash', 18446744073709551615);
    END;
    IF actual_errno <> expected_errno THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Unknown role reference must raise MySQL error 1452';
    END IF;

    SET expected_errno = 3819;
    SET actual_errno = 0;
    BEGIN
        DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            GET DIAGNOSTICS CONDITION 1 actual_errno = MYSQL_ERRNO;
        END;
        INSERT INTO `Role` (role_name) VALUES ('Invalid Role');
    END;
    IF actual_errno <> expected_errno THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid role must raise MySQL error 3819';
    END IF;

    SET expected_errno = 1048;
    SET actual_errno = 0;
    BEGIN
        DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            GET DIAGNOSTICS CONDITION 1 actual_errno = MYSQL_ERRNO;
        END;
        INSERT INTO `Role` (role_name) VALUES (NULL);
    END;
    IF actual_errno <> expected_errno THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'NULL role_name must raise MySQL error 1048';
    END IF;

    SET expected_errno = 1062;
    SET actual_errno = 0;
    BEGIN
        DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            GET DIAGNOSTICS CONDITION 1 actual_errno = MYSQL_ERRNO;
        END;
        INSERT INTO `Role` (role_name) VALUES ('Volunteer');
    END;
    IF actual_errno <> expected_errno THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Duplicate role_name must raise MySQL error 1062';
    END IF;

    SET expected_errno = 1451;
    SET actual_errno = 0;
    BEGIN
        DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            GET DIAGNOSTICS CONDITION 1 actual_errno = MYSQL_ERRNO;
        END;
        DELETE FROM `Role` WHERE role_id = volunteer_role_id;
    END;
    IF actual_errno <> expected_errno THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Referenced role delete must raise MySQL error 1451';
    END IF;

    DELETE FROM `User` WHERE user_id IN (test_user_id, updated_user_id);
    SELECT COUNT(*) INTO actual_count
    FROM `User`
    WHERE user_id IN (test_user_id, updated_user_id);
    IF actual_count <> 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User delete failed';
    END IF;

    ROLLBACK;
END$$
DELIMITER ;

CALL run_increment_1_smoke_tests();
SELECT 'PASS: Increment 1 database smoke tests' AS test_result;
DROP PROCEDURE run_increment_1_smoke_tests;

-- Reconnect persistence is intentionally not asserted: this script runs in a
-- single MySQL session. Verify persistence by querying a committed fixture
-- from a second mysql session if that behavior needs an integration test.
