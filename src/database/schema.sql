-- Event & Volunteer Management System
-- MySQL 8.0.16+ (CHECK constraints are enforced from 8.0.16).
-- This schema implements the current Increment 1 ERD: Role, User, UserSession.

CREATE DATABASE IF NOT EXISTS event_volunteer_management
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE event_volunteer_management;

CREATE TABLE IF NOT EXISTS roles (
    role_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    role_name VARCHAR(30) NOT NULL,
    PRIMARY KEY (role_id),
    CONSTRAINT uq_roles_role_name UNIQUE (role_name),
    CONSTRAINT chk_roles_role_name CHECK (
        role_name IN ('Administrator', 'Event Organizer', 'Volunteer')
    )
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id BIGINT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id),
    CONSTRAINT uq_users_email UNIQUE (email),
    CONSTRAINT chk_users_full_name CHECK (CHAR_LENGTH(TRIM(full_name)) > 0),
    CONSTRAINT chk_users_email_nonempty CHECK (CHAR_LENGTH(TRIM(email)) > 0),
    CONSTRAINT chk_users_password_hash_nonempty CHECK (CHAR_LENGTH(password_hash) > 0),
    KEY ix_users_role_id (role_id),
    CONSTRAINT fk_users_role
        FOREIGN KEY (role_id) REFERENCES roles (role_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS user_sessions (
    session_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    token_hash CHAR(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    revoked_at DATETIME NULL DEFAULT NULL,
    PRIMARY KEY (session_id),
    CONSTRAINT uq_user_sessions_token_hash UNIQUE (token_hash),
    CONSTRAINT chk_user_sessions_expiry CHECK (expires_at > created_at),
    CONSTRAINT chk_user_sessions_revoked CHECK (revoked_at IS NULL OR revoked_at >= created_at),
    KEY ix_user_sessions_user_expiry (user_id, expires_at),
    KEY ix_user_sessions_active_expiry (expires_at, revoked_at),
    CONSTRAINT fk_user_sessions_user
        FOREIGN KEY (user_id) REFERENCES users (user_id)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;
