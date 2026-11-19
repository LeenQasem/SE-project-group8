# Increment 1 Initial ERD: Prompt Record

## Section 3.3 Metadata

- **Project / Increment:** Event & Volunteer Management System — Increment 1: Authentication and User Management
- **Version:** v0.1.0-design
- **Task version:** v0.1.0-design
- **Coding agent:** Codex
- **Objective:** Define the initial relational data model for Increment 1 account registration, authentication, administrator account management, and role-based authorization.
- **Requirements:** FR-01, FR-02, FR-03, FR-04, FR-20; NFR-10, NFR-12, NFR-14, NFR-15.
- **References:** `docs/requirements.md`; `docs/incremental_development_plan.md` (Increment 1 design scope and acceptance criteria); `docs/architecture.md` (MySQL data tier); `uml/class_diagram.puml`; `uml/increment_1_authentication_user_management_activity.puml`.
- **Intended outputs:** PlantUML source, rendered SVG and PNG, and this prompt record.

## Task and design decisions

Create an initial ERD for Increment 1 only. Model `User` and `Role`, their keys, registration and login attributes, uniqueness constraints, relationship cardinality, and the restriction that public registration creates Volunteer accounts only. Exclude Event, Application, Task, and Attendance because they belong to later increments.

- A user has exactly one role; a role may be assigned to zero or many users. This follows the singular `User.role` and one-to-one role association in `uml/class_diagram.puml`.
- Use `role_id` as the `User` foreign key and unique `role_name` values for Administrator, Event Organizer, and Volunteer.
- Public registration is restricted to Volunteer. Privileged role assignment is through administrator account management.
- Store only a password hash, never a plain-text password. The diagram labels it as a salted, one-way hash per NFR-10.
- `email` is unique, consistent with the existing registration activity diagram's duplicate-email check. Attribute lengths and `BIGINT` key types are MySQL-oriented design choices, not values specified by requirements.
- No permission table or account status field was added because the project documentation does not define their structure or values. Access control is enforced by role as required by FR-04 and NFR-12.

## Validation and result paths

- `uml/increment_1_initial_erd.puml`
- `uml/rendered/increment_1_initial_erd.svg`
- `uml/rendered/increment_1_initial_erd.png`

The SVG was parsed as valid XML, the PNG was verified as a valid 1500 × 950 image, and the PNG was visually inspected for readability, cardinality labels, and layout. The PNG and SVG were generated locally from the same ERD content. PlantUML itself was not available locally, and a request to the public PlantUML renderer returned HTTP 403; therefore PlantUML-engine syntax validation and native PlantUML rendering remain unverified. This record does not claim those checks passed.

## Acceptance criteria

- The diagram shows the User and Role entities, PK/FK markers, data types, and a unique email constraint.
- It represents exactly one role per user and zero or more users per role.
- It supports the three documented roles and prevents public registration from assigning privileged roles.
- It shows secure password-hash storage and excludes entities belonging to later increments.
- Rendered files are present and readable; validation limitations are stated accurately.

## Documentation observations

- `docs/requirements.md` says FR-01 permits account creation but does not itself specify volunteer-only public registration. The Increment 1 plan says registration includes volunteers, and the existing activity diagram explicitly assigns Volunteer during public registration; this ERD follows those design artifacts.
- The role model is singular in the existing class diagram, so multi-role assignments are not modeled.
- NFR-14 requires security-event logging, but no audit-log schema is defined in the Increment 1 entity list or architecture data model; no additional audit entity was invented here.
