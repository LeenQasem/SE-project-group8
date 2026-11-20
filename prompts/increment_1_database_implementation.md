# Task: Implement the Database for Increment 1 – Event & Volunteer Management System

You are working on our Event & Volunteer Management System university Software Engineering project.

Your task is to **fully design, implement, configure, and test the database required for Increment 1**, ensuring that it is functional, consistent with our finalized project documentation, and structured in a way that supports future increments.

This is an implementation task, not merely a database design or code-generation exercise.

## 1. First: Understand the Existing Project

Before writing or modifying any code, carefully inspect the repository.

Locate and study the following files and resources:

- `requirements.md`
- `incremental_development_plan.md`
- The finalized ERD and any related UML diagrams.
- Existing source code and project structure.
- Existing database configuration, if any.
- Existing documentation and README files.
- The `prompts` folder and its existing prompt files.

Pay particular attention to the first increment in the incremental development plan.

Use the repository's actual documentation as the source of truth. Do not assume functionality belongs to Increment 1 simply because it appears somewhere in the complete requirements document.

Understand:
- The system's purpose.
- The three user roles: Admin, Event Organizer, and Volunteer.
- The functionality assigned to each role in Increment 1.
- The entities, attributes, relationships, and constraints in the ERD.
- The distinction between functionality introduced in Increment 1 and functionality reserved for later increments.

Do not start implementation until you understand these elements.

## 2. Scope: Increment 1 Only

Implement the database functionality required for the first increment.

The database must support all the requirements and use cases assigned to Increment 1.

Important incremental development rules:

- Increment 1 must be independently functional.
- Do not implement features belonging exclusively to Increment 2 or later.
- Do not introduce unnecessary tables or functionality from future increments.
- However, avoid architectural decisions that would make future increments difficult to integrate.
- The database should be extendable as the system grows.
- Do not remove or break existing project functionality.

Increment 2 and subsequent increments will extend the same system and database rather than create separate systems.

## 3. Database Design and Implementation

Translate the finalized ERD into a working relational database.

Implement all database elements required by Increment 1, including:

### A. Tables and attributes
- Create all necessary tables.
- Include all required attributes.
- Choose appropriate database data types.
- Define suitable primary keys.
- Define foreign keys wherever relationships require them.
- Apply NOT NULL constraints where appropriate.
- Apply UNIQUE constraints where required.
- Implement DEFAULT values where appropriate.
- Apply CHECK constraints where supported and relevant.

### B. Relationships
Ensure that all implemented relationships accurately reflect the ERD.

Pay attention to:
- One-to-one relationships.
- One-to-many relationships.
- Many-to-many relationships.
- Referential integrity.
- Appropriate foreign-key behavior.
- Optional versus mandatory relationships.

For many-to-many relationships, implement appropriate junction tables.

Do not arbitrarily change the ERD's relationships.

If you discover an inconsistency between the ERD and the requirements, document it and explain the issue before making any significant design change.

### C. User roles and authentication-related data

Implement the database structures needed for the user-related functionality in Increment 1.

The system has three roles:
- Admin
- Event Organizer
- Volunteer

Ensure that:
- User roles are represented consistently.
- The database prevents invalid role values.
- User information is stored appropriately.
- Email uniqueness is enforced if required.
- Passwords are never stored in plaintext.
- Only password hashes are stored.
- The schema can support role-based authorization in the application.

Do not implement unnecessary authentication features outside Increment 1.

### D. Data integrity

Ensure the database protects against invalid or inconsistent data.

Consider:
- Foreign-key integrity.
- Duplicate records.
- Invalid values.
- Missing required information.
- Invalid relationships.
- Appropriate deletion and update behavior.

Use sensible database-level constraints rather than relying exclusively on application code.

## 4. Database Architecture and Code Quality

Follow the technology stack and conventions already established in the repository.

Do not introduce a different database engine, programming language, ORM, or framework without a compelling reason.

If the project does not yet have a database technology established, select an appropriate solution based on the existing application architecture and document the decision.

Organize the implementation cleanly.

Where appropriate, include:
- Database configuration.
- Connection management.
- Schema creation or migrations.
- Database models or entities.
- Repositories or data-access layers.
- Initialization scripts.
- Seed data.
- Database utilities.

Avoid:
- Duplicated database logic.
- Hardcoded credentials.
- Unnecessary dependencies.
- Unstructured SQL.
- Unnecessary abstraction.
- Mixing database responsibilities with unrelated application logic.

Use environment variables for sensitive configuration and provide an appropriate `.env.example` if needed. Never commit actual credentials.

## 5. Database Initialization and Sample Data

Make it possible to initialize the database reliably from a clean environment.

Provide the necessary scripts or commands to:

1. Configure the database.
2. Create the database schema.
3. Apply migrations, if applicable.
4. Insert appropriate initial or sample data.
5. Verify that initialization completed successfully.

Sample data should be realistic and consistent with the system's requirements.

Include examples of the relevant user roles where appropriate.

Ensure that initialization can be repeated safely without creating duplicate records or corrupting existing data.

Do not insert fake production credentials or plaintext passwords.

## 6. Functional Database Operations

The database must not simply contain tables that look correct. It must actually work.

Implement the database operations required by the first increment.

These should be derived from the actual Increment 1 requirements.

Depending on the functionality included in Increment 1, this may involve:

- Creating records.
- Retrieving records.
- Updating records.
- Deleting records where permitted.
- Searching or filtering records.
- Retrieving related records through relationships.

Do not implement operations for features that belong exclusively to future increments.

Make sure that database operations handle errors appropriately and do not silently accept invalid data.

## 7. Testing and Verification

Thoroughly test the database implementation.

Include tests for:

- Successful database initialization.
- Successful table creation.
- Primary-key constraints.
- Foreign-key constraints.
- Unique constraints.
- Required attributes.
- Valid and invalid role values.
- Correct relationship behavior.
- Successful CRUD operations required by Increment 1.
- Handling of invalid or duplicate data.
- Persistence of data after reconnecting to the database.

Test both successful and unsuccessful scenarios.

Use an isolated test database where appropriate so tests do not damage actual development data.

Do not claim that something works unless you have actually tested it.

Fix any discovered issues before considering the task complete.

## 8. Documentation

Document the database implementation.

Create or update the appropriate documentation to explain:

- Which database technology is being used.
- How the database is structured.
- Which tables are implemented.
- Important relationships and constraints.
- How the database is initialized.
- How sample data is inserted.
- How to run the database.
- How to run the tests.
- Any assumptions or implementation decisions.

Keep the documentation consistent with the actual implementation.

Do not unnecessarily rewrite unrelated documentation.

## 9. Important Project Constraints

Follow these rules throughout the task:

1. Treat `requirements.md` and `incremental_development_plan.md` as finalized project documents.
2. Use the finalized ERD as the main reference for database structure.
3. Do not silently change requirements or relationships.
4. Implement only Increment 1 functionality.
5. Preserve compatibility with future increments.
6. Follow the existing repository's coding conventions.
7. Do not overwrite unrelated files.
8. Do not delete existing work.
9. Do not modify unrelated UML diagrams or project documentation.
10. Do not create unnecessary features just to make the implementation appear more complete.

Before making changes, inspect the Git working tree and preserve all existing uncommitted work. Do not reset, clean, or discard changes. Do not commit or push anything.

## 10. Save This Prompt in the Repository

In addition to implementing the database, save this entire prompt as a separate Markdown file inside the existing `prompts` folder.

Instructions:

- Inspect the existing prompt files first.
- Follow their naming conventions.
- Follow their formatting and organization.
- Use a descriptive filename, such as `increment_1_database_implementation.md`, unless the repository uses a different naming convention.
- Do not overwrite any existing prompt.
- Preserve the existing prompt files.
- Save the complete prompt, not an abbreviated version.

The prompt file should be committed to the repository only as a normal project file change; do not perform a Git commit yourself.

## 11. Final Verification and Report

When implementation is complete, provide a clear summary containing:

1. Database technology used.
2. Tables created.
3. Relationships implemented.
4. Constraints and integrity rules implemented.
5. Database initialization instructions.
6. Sample data included.
7. Database operations implemented.
8. Tests executed and their actual results.
9. Files created or modified.
10. Location of the saved prompt.
11. Any remaining issues or assumptions.

Explicitly distinguish between:
- Fully implemented and tested functionality.
- Implemented but not fully tested functionality.
- Functionality intentionally deferred to later increments.

If something cannot be implemented because the documentation is ambiguous or contradictory, explain the issue instead of inventing a solution.

## Final Objective

Deliver a clean, functional, tested, and maintainable database implementation that satisfies **all database-related requirements of Increment 1** of our Event & Volunteer Management System.

The result should integrate naturally with the existing repository, respect the finalized ERD and requirements, and provide a reliable foundation for Increment 2 and subsequent increments.