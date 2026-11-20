# System Architecture — Increment 1 (v0.1.0)

## Scope and technology

This repository describes the planned Event & Volunteer Management System. The project description selects a React browser client, Node.js/Express API, and MySQL database. This checkout currently contains design artifacts only; it has no application source, dependency manifest, migration, or executable test suite. Diagrams are design intent and do not claim implementation is complete.

Increment 1 includes **UC01 User Account & Authentication**, **UC02 User Management & RBAC**, and persistence for `users` and `user_sessions`. UC03–UC07 (events, exploration/applications, task assignment, attendance/hours, and statistics) are deferred to Increment 2. The deferred actors remain shown where useful for system context, but their workflows and data are outside v0.1.0.

## Logical layers

1. **Presentation / Boundary:** React UI calls `AuthController` and `AdminUserController` over HTTPS/JSON.
2. **Application / Services:** `AuthService` handles registration, credential checks, session lifecycle; `UserManagementService` handles account listing/view/update and role changes; `AccessControlService` validates sessions and authorizes administrator operations.
3. **Data Access:** `UserRepository` issues parameterized MySQL operations for users and sessions.
4. **Domain:** `User`, `UserSession`, `UserRole`, and `AccountStatus` define account and session state.

MySQL contains `users` and `user_sessions` tables. Email verification is an optional external integration. Daily backups and restore procedures target Cloud Backup Storage under NFR-02 and NFR-03; they are persistence/operations concerns and do not add later-increment business entities.

## Registration, roles, and session policy

Public registration accepts name, email, password. The backend validates and sanitizes fields, enforces valid unique email, hashes passwords with a salted one-way algorithm (NFR-10), and always sets role `VOLUNTEER`; any submitted role field is ignored. Passwords are never persisted in plaintext. Sessions store a token hash, expiry, and optional revocation timestamp.

The first Administrator is provisioned manually through a guarded setup command, not a public API. The setup requires a protected one-time secret, refuses to proceed if an Administrator already exists, serializes concurrent attempts with a database lock/transaction, and consumes the one-time authorization. After bootstrap, only an authenticated Administrator may assign/change roles or update permitted account fields. Backend authorization is mandatory (FR-04, NFR-12). Public registration cannot create Administrator or Event Organizer accounts.

The detailed provisioning secret-delivery mechanism remains a deployment decision and must be documented before implementation. Never log passwords, session tokens, or bootstrap secrets (NFR-14, NFR-20).

## Persistence and security

`users.email` has a unique constraint; `users.role` is a required enum with exactly the three supported roles; user/session rows have primary keys and timestamps. `user_sessions.user_id` references `users.id`, and session token hashes are unique. Expired/revoked sessions cannot authenticate. Use HTTPS/TLS in transit, restricted database access and appropriate encryption/access controls at rest (NFR-11). Use parameterized SQL, generic login errors, field-level validation feedback, and security/audit events without secrets (NFR-05, NFR-13, NFR-14, NFR-18).

NFR-01 supplies a login latency target; it requires measurement once implementation exists. Responsive behavior and common navigation are frontend requirements (NFR-16, NFR-17). Automated tests are required by NFR-21 but cannot be claimed until application code and tests exist.

## Increment 2 boundary

`Event`, `Application`, `Task`, and `Attendance` and the UC03–UC07 services/repositories are deferred. They appear only as planned context; they are not part of the v0.1.0 persistence schema or implementation scope.

## Diagram sources and rendering

Editable sources: `uml/use_case.puml`, `uml/class_diagram.puml`, `uml/sequence_diagram.mmd`, `uml/sequence_auth.mmd`, `uml/sequence_admin_rbac.mmd`, `uml/system_context.puml`, `uml/container.puml`, `uml/component.puml`, `uml/deployment.puml`, `uml/activity_increment1.puml`, `uml/activity_admin_rbac.puml`, and `uml/erd_increment1.puml`.

From the repository root, after installing Java and downloading `plantuml.jar` plus Mermaid CLI (`@mermaid-js/mermaid-cli`):

```powershell
New-Item -ItemType Directory -Force uml/rendered | Out-Null
java -jar plantuml.jar -tpng -o rendered uml/use_case.puml uml/class_diagram.puml uml/system_context.puml uml/container.puml uml/component.puml uml/deployment.puml uml/activity_increment1.puml uml/activity_admin_rbac.puml uml/erd_increment1.puml
npx mmdc -i uml/sequence_diagram.mmd -o uml/rendered/sequence-diagram.png
npx mmdc -i uml/sequence_auth.mmd -o uml/rendered/sequence_auth.png
npx mmdc -i uml/sequence_admin_rbac.mmd -o uml/rendered/sequence_admin_rbac.png
```

PlantUML C4 sources use the C4-PlantUML standard library include URL and therefore need network access when the library is not cached. Output PNGs are design renders, not execution evidence.

