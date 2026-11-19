# Increment 1 Class Diagram Prompt Record

## Metadata

- **Version / Increment:** v0.1.0-design — Authentication and User Management
- **Agent:** Codex
- **Goal:** Produce an Increment 1 only class diagram consistent with requirements, architecture, overall class model, and initial ERD.
- **References reviewed:** `docs/requirements.md`, `docs/architecture.md`, `docs/incremental_development_plan.md`, `uml/class_diagram.puml`, `uml/ERD_increment1.puml`, `uml/Activity_increment1.puml`, and relevant prompt records in `prompts/`.
- **Outputs:** `uml/class_diagram_increment1.puml`, `uml/class_diagram_increment1.png` (render requested; unavailable in this environment), and this record.

## Scope and decisions

The diagram covers FR-01 through FR-04, FR-20, and NFR-10: account registration, authentication/session lifecycle, the three roles, role-based authorization, administrator user/organizer account management, and secure password-hash storage.

The model retains a single `User` with one `UserRole`, consistent with the ERD and overall class diagram. Public registration assigns Volunteer; administrator account management handles organizer accounts. `UserSession` represents the session lifecycle required by FR-02, without inventing persistence fields, token format, expiration policy, or an `AccountStatus` field/enum. The ERD explicitly omits account status and the repository does not define a session schema. Presentation, application-service, and data-access classes follow the architecture's three-tier/API and data-access boundaries; their operations are limited to the requested Increment 1 behaviors.

Event, Application, Task, and Attendance are excluded as later-increment concepts.

## Validation

PlantUML source structure and requirement traceability were reviewed. A PlantUML executable, Java runtime, and image renderer were not available in the environment, so no PNG was generated or visually inspected. Do not treat the requested PNG as complete until rendered and reviewed.
