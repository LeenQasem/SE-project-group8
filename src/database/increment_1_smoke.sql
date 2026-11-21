-- Increment 1 smoke checks. Run after schema.sql and seed.sql.
-- All probe rows are rolled back. Requires MySQL 8.0.16+.
USE event_volunteer_management;

DELIMITER //
CREATE PROCEDURE run_increment_1_smoke()
BEGIN
    DECLARE test_user_id BIGINT UNSIGNED;
    DECLARE volunteer_role_id BIGINT UNSIGNED;
    DECLARE organizer_role_id BIGINT UNSIGNED;
    DECLARE created_session_id BIGINT UNSIGNED;
    DECLARE caught_error BOOLEAN DEFAULT FALSE;
    DECLARE missing_role_rejected BOOLEAN DEFAULT FALSE;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;
    SELECT role_id INTO volunteer_role_id
    FROM roles WHERE role_name = 'Volunteer';

    IF volunteer_role_id IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'FAIL: Volunteer seed role missing';
    END IF;

    -- The same scalar role lookup used by registration must fail closed when
    -- the requested role does not exist, rather than completing a zero-row INSERT.
    BEGIN
        DECLARE CONTINUE HANDLER FOR 1048 SET missing_role_rejected = TRUE;
        INSERT INTO users (full_name, email, password_hash, role_id)
        VALUES ('Missing Role Probe', 'missing.role.increment1@example.invalid',
                'NOT_A_LOGIN_CREDENTIAL_SMOKE_FIXTURE',
                (SELECT role_id FROM roles WHERE role_name = '__missing_role_probe__'));
    END;
    IF missing_role_rejected = FALSE THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'FAIL: missing role was not rejected';
    END IF;
    IF (SELECT COUNT(*) FROM users
        WHERE email = 'missing.role.increment1@example.invalid') <> 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'FAIL: user inserted without required role';
    END IF;

    INSERT INTO users (full_name, email, password_hash, role_id)
    VALUES ('Smoke Test Volunteer', 'smoke.increment1@example.invalid',
            'NOT_A_LOGIN_CREDENTIAL_SMOKE_FIXTURE', volunteer_role_id);
    SET test_user_id = LAST_INSERT_ID();

    IF (SELECT COUNT(*) FROM users WHERE user_id = test_user_id) <> 1 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'FAIL: user create/read check';
    END IF;

    -- Duplicate email must be rejected by the UNIQUE constraint.
    BEGIN
        DECLARE CONTINUE HANDLER FOR 1062 SET caught_error = TRUE;
        INSERT INTO users (full_name, email, password_hash, role_id)
        VALUES ('Duplicate Probe', 'smoke.increment1@example.invalid', 'probe', volunteer_role_id);
    END;
    IF caught_error = FALSE THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'FAIL: duplicate email was accepted';
    END IF;

    INSERT INTO user_sessions (user_id, token_hash, expires_at)
    VALUES (test_user_id, REPEAT('a', 64), DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 1 HOUR));
    SET created_session_id = LAST_INSERT_ID();

    UPDATE user_sessions SET revoked_at = CURRENT_TIMESTAMP
    WHERE session_id = created_session_id;
    IF (SELECT revoked_at IS NULL FROM user_sessions WHERE session_id = created_session_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'FAIL: session revoke check';
    END IF;

    UPDATE users SET full_name = 'Updated Smoke Volunteer' WHERE user_id = test_user_id;
    IF (SELECT full_name FROM users WHERE user_id = test_user_id) <> 'Updated Smoke Volunteer' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'FAIL: user update check';
    END IF;

    SELECT role_id INTO organizer_role_id
    FROM roles WHERE role_name = 'Event Organizer';
    IF organizer_role_id IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'FAIL: Event Organizer seed role missing';
    END IF;
    UPDATE users SET role_id = organizer_role_id WHERE user_id = test_user_id;
    IF (SELECT role_id FROM users WHERE user_id = test_user_id) <> organizer_role_id THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'FAIL: role assignment check';
    END IF;

    ROLLBACK;
    SELECT 'PASS: Increment 1 user create/read/update, role assignment, duplicate and missing-role rejection, session create/revoke' AS result;
END//
DELIMITER ;

CALL run_increment_1_smoke();
DROP PROCEDURE run_increment_1_smoke;
