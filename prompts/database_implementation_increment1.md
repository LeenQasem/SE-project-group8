# Increment 1 Database Implementation Prompt

## Objective

Create the MySQL database implementation for the Event & Volunteer Management System's first development increment: Authentication and User Management.

## Sources

- `docs/requirements.md`
- `docs/incremental_development_plan.md`
- `docs/architecture.md`
- `docs/traceability_matrix.md`
- `uml/erd_increment1.puml`
- Existing database conventions and documentation in the repository

Use the ERD as the primary reference for entities, attributes, keys, and relationships. Use requirements and workflow documents to clarify database behavior. Record any disagreements among sources without changing approved diagrams or requirements.

## Scope and constraints

- Implement the approved Increment 1 schema in MySQL. Use suitable primary and foreign keys, constraints, indexes, data types, and deletion rules.
- Include the approved account, role, and authentication/session data only. Do not add entities solely because they are common in similar systems.
- Keep the schema suitable for the later increments without implementing their backend or frontend operations.
- Provide parameterized SQL examples for Increment 1 account and authentication operations, fictional development seed data, and a practical Increment 1 smoke script.
- Store only application-generated salted one-way password hashes. Never put plaintext passwords in SQL seed data.
- Use transactions where related database writes must succeed or fail together.
- Use MySQL-compatible SQL only. Do not create Python, Flutter, or other application code.
- Do not modify approved requirements or diagrams. Do not execute destructive operations against shared or production databases.

## Deliverables

- `database/schema.sql`
- `database/operations.sql`
- `database/seed.sql`
- `database/increment_1_smoke.sql`
- `database/README.md`
- Update the main README, traceability, and AI development log only where their database references require it.

## Verification and reporting

Run the schema, seed, and smoke SQL against local MySQL when available. Report actual results and limitations; do not claim tests passed without execution. Explain the tables and relationships, their ERD correspondence, Increment 1 coverage, and any unresolved design conflicts.
