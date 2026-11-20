# Codex Task: Improve Increment 1 Database Smoke Tests

You are working on our Event & Volunteer Management System (EVMS) repository.

Your task is to improve the existing `increment_1_smoke.sql` file so that it provides meaningful, automated verification of the Increment 1 database implementation.

You must also document this task by adding an appropriate prompt to the existing database prompt file/folder, following the exact organization and formatting conventions already used in the repository.

## 1. IMPORTANT: Understand the Existing Project Before Making Changes

Before modifying anything, inspect and understand the following existing project files:

- The finalized project requirements document.
- The finalized incremental development plan.
- The finalized Increment 1 ERD.
- The finalized Increment 1 class diagram.
- The existing database implementation files:
  - `schema.sql`
  - `seed.sql`
  - `operations.sql`
  - `increment_1_smoke.sql`
  - `README.md`
- The existing database-related Codex prompts and their folder structure.

Treat these documents as the authoritative source of truth.

**Do not independently redesign, reinterpret, or extend the approved project scope.**

If you discover inconsistencies between the existing implementation and the approved diagrams or requirements, document them instead of silently changing the design.

## 2. Main Objective: Improve increment_1_smoke.sql

Review the existing smoke test and improve it so that it automatically verifies the actual behavior and integrity of the Increment 1 database.

The current smoke test checks whether:

- The three required roles exist.
- The `User` table exists.
- The `Role` table exists.

It also contains manual negative-test instructions in comments.

Your objective is to turn the relevant manual checks into automated tests wherever practical.

## 3. Required Test Coverage

The improved smoke test should cover the following areas.

### A. Database structure

Verify that:

- Both `User` and `Role` tables exist.
- The three expected roles exist:
  - Administrator
  - Event Organizer
  - Volunteer
- The database contains the expected columns.
- Primary keys, unique constraints, and foreign-key relationships are correctly defined.
- The email uniqueness constraint exists.
- Required fields have the expected NOT NULL restrictions.

## Follow-up refinements

When revising the smoke test:

- Check that all required Increment 1 columns and their expected types exist, but do not require the `User` or `Role` tables to contain exactly seven columns. Later approved increments may add columns.
- Keep the required-column, type, primary-key, unique-key, foreign-key, and NOT NULL checks intact.
- In negative tests, capture and assert the expected MySQL error number where practical. Do not count an unrelated `SQLEXCEPTION` as a passing constraint test; fail on an unexpected error.
- Preserve successful CRUD checks, rollback behavior, and temporary test data handling.
- Document a repeatable `seed.sql` idempotency check in the database README, separate from the main smoke test. Verify the three role rows remain unique after repeated seed execution.
- Do not modify the schema, seed data, operations, ERD, class diagram, requirements, or incremental development plan.
- Report Git diff changes and do not claim MySQL runtime validation unless the tests were actually run against MySQL 8.0.16 or newer.
