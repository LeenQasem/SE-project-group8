# Increment 1 database

## Scope and design

This repository documents a React / Node.js / Express / MySQL system, but does not yet contain application code or a database driver. Increment 1's finalized ERD (`uml/ERD_increment1.puml`) defines only `Role` and `User`; this implementation does not add event, application, task, attendance, audit-log, or persisted-session tables. Login sessions remain an application concern because the ERD does not model them.

The schema targets MySQL 8.0.16 or newer, InnoDB, and `utf8mb4`. It implements the ERD's BIGINT primary keys, unique role names and emails, one mandatory role per user, and referential integrity. A check constraint limits roles to Administrator, Event Organizer, and Volunteer. Email uniqueness uses the database's case-insensitive default collation; the application should also normalize email input consistently. The database stores only a `password_hash`; the not-yet-implemented backend must compute and verify a salted, one-way password hash and must never pass a plaintext password to SQL.

The ERD and activity diagram assign Volunteer to public registrations. The SQL registration example fixes this role. The database permits the other two role values for administrator account management; enforcing that only an authorized administrator may change roles belongs in the backend's authorization layer.

## Unresolved documentation point

The Increment 1 plan maps NFR-14 (security event logging) into the working increment, while the finalized initial ERD and its prompt record do not define an audit-log entity or its fields. This implementation does not invent an audit schema; the team should reconcile the NFR-14 data model before implementing that requirement. The account schema itself covers FR-01 through FR-04 and the user/role data needed by FR-20.

## Initialize a clean local database

Install MySQL Server and its command-line client (8.0.16+). Create a database using a MySQL administrative account:

```sql
CREATE DATABASE evms CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
```

From a shell whose input redirection is supported, apply the schema, then seed the role reference rows:

```sh
mysql -u <database-user> -p evms < database/schema.sql
mysql -u <database-user> -p evms < database/seed.sql
```

The schema uses `CREATE TABLE IF NOT EXISTS`; the role seed is safe to run repeatedly. The script does not create database accounts or embed credentials. Configure a least-privilege application database account and its connection settings in the future backend's environment configuration; never commit real credentials.

## Sample data

`seed.sql` inserts the three required role rows only. It intentionally creates no user accounts, sample passwords, or fake production credentials. Create users through the application using valid password hashes.

## Data operations

`operations.sql` contains parameterized MySQL statements for volunteer registration, lookup for password verification, loading a user's role, administrator user listing, profile/password updates, role changes, and deletion. Bind parameters through the backend's MySQL driver. Check affected-row counts and translate duplicate-email and other database errors into safe application messages. Authorization, password verification, session lifecycle, and volunteer-only public registration are application responsibilities.

## Verification

After applying schema and seed to a **disposable test database**, run:

```sh
mysql -u <test-database-user> -p evms_test < database/tests/increment_1_smoke.sql
```

The smoke script checks role seed and table presence. Its comments list additional negative constraint checks to perform manually. This repository has no MySQL client or server available in the current environment, so SQL execution, CRUD behavior, constraint failures, and reconnect persistence have not been verified here. Run those checks against a local MySQL instance before treating the database as runtime-validated. The test script creates and drops a temporary stored procedure, so run it only in a disposable test database.

## Future increments

Increment 2 and later should extend this same MySQL database with their approved ERD changes. Do not treat this initial schema as a separate system or add later-increment tables before their designs are approved.
