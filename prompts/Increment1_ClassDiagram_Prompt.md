# Increment 1 UML Class Diagram Prompt

## Objective

Create an increment-specific UML class diagram for the Event & Volunteer Management System, limited to `v0.1.0-design` authentication and user management.

## Sources to examine

- `docs/requirements.md`
- `docs/architecture.md`
- `docs/incremental_development_plan.md`
- `uml/class_diagram.puml`
- `uml/ERD_increment1.puml`
- `uml/Activity_increment1.puml`
- Existing UML prompt records under `prompts/`

## Scope

Represent account registration, login/logout and session lifecycle (FR-01, FR-02), the three supported user roles (FR-03), role authorization (FR-04), administrator management of user and organizer accounts (FR-20), and secure password hashing (NFR-10). Include only classes and relationships relevant to this increment. Exclude Event, Application, Task, Attendance, and all later-increment behavior.

Use the architecture's presentation, application, and data-access boundaries. Show typed attributes and operations, visibility, dependencies/associations, and meaningful multiplicities. Apply restrained academic styling and arrange the diagram for legibility.

## Design constraints

- Keep one `User` with one `UserRole`, consistent with the initial ERD and overall class model; do not duplicate roles as subclasses.
- Public registration assigns Volunteer; privileged organizer account management is administrator-controlled.
- Store a password hash, never a plain-text password.
- The ERD does not define `AccountStatus` or persisted session/token fields. Do not add those fields or a status enum. Model session lifecycle only to the extent required by FR-02.
- Do not alter the overall class diagram.

## Deliverables and verification

Save `Increment1_ClassDiagram.puml` and its corresponding PNG in `uml/`; save this prompt as `prompts/Increment1_ClassDiagram_Prompt.md`. Compare included elements with the overall diagram, ERD, requirements, and Increment 1 plan. Render and inspect the PNG, and report any renderer or validation limitation accurately.
