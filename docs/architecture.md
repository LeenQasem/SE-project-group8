# System Architecture — Increment 1 (v0.1.0-design)

## Scope and technology

The Event & Volunteer Management System is planned as a React browser client, Node.js/Express backend, and MySQL database. This repository contains design artifacts only; it has no application source, dependency manifest, database migration, or executable application tests. The diagrams describe intended design and do not claim implementation is complete.

Increment 1 covers **UC01 User Account & Authentication**, **UC02 User Management & RBAC**, and persistence for the **`users` table only**: `id`, `name`, `email`, `password_hash`, `role`, `created_at`, and `updated_at`. `role` is one of `ADMINISTRATOR`, `EVENT_ORGANIZER`, or `VOLUNTEER`. UC03–UC07 are deferred across Increments 2–4 (`v0.2.0`–`v0.4.0`): Events & Exploration; Applications, Tasks & Attendance; and Statistics & Analytics.

## Simplified architectural structure

1. **Presentation / Boundary (React UI):** Provides registration, login/logout, and administrator user-management screens. It communicates with the backend API over HTTPS/JSON.
2. **Control Layer:** `AuthController` handles `register()`, `login()`, and `logout()`. `AdminUserController` handles administrator-only `viewUsers()` and `assignRole()` operations.
3. **Domain / Entity Layer:** `User` holds `id`, `name`, `email`, `passwordHash`, and `role`; its helper methods are `verifyPassword()` and `hasRole()`. `UserRole` defines the three supported roles.
4. **Persistence (MySQL):** Stores the `users` table with a unique email, salted one-way `password_hash`, and role enum.

## Registration, roles, and stateless authentication

Public registration accepts a name, email, and password. The backend validates and sanitizes the input, enforces valid unique email, hashes the password using a salted one-way algorithm (NFR-10), and always assigns `VOLUNTEER`. It ignores or rejects any client-supplied role. Plaintext passwords are never stored.

`AuthController.login()` issues a signed, expiring JWT in a `Secure`, `HttpOnly`, `SameSite` cookie after verifying the password hash. Authentication state is stateless: there is no separate session entity or session table. `AuthController.logout()` clears the authentication cookie. Expired or invalid signatures are rejected.

The first Administrator is created manually through a guarded one-time setup, never through public registration. Setup requires protected one-time authorization, refuses to run if an Administrator already exists, serializes concurrent attempts, and consumes the authorization. Thereafter, only an authenticated Administrator may call `AdminUserController.assignRole()`. The backend validates the requested value against `UserRole` and uses `User.hasRole()` for RBAC checks (FR-04, NFR-12). Public registration cannot grant Administrator or Event Organizer privileges.

## Persistence and security

The `users` table has a primary key, unique `email`, required `password_hash`, required `role` enum, and creation/update timestamps. The role enum permits exactly the three supported values. MySQL access is limited to the backend and uses parameterized statements. HTTPS/TLS protects data in transit; appropriate encryption or access controls protect data at rest (NFR-11).

Use safe user-facing errors without exposing internal details (NFR-05), validate and sanitize inputs (NFR-13), record security-relevant events without passwords or authentication secrets (NFR-14, NFR-20), and collect only necessary account data (NFR-15). Responsive UI, consistent navigation, and field-level validation feedback are required (NFR-16–NFR-18). The login performance target (NFR-01) and automated auth/RBAC tests (NFR-21) require verification when implementation exists. Backup and recovery constraints (NFR-02, NFR-03) are operational requirements and do not add tables to the Increment 1 account model.

Email Service notifications, including registration verification and application status messages, are deferred to later increments; email is not part of Increment 1 account registration. Provider selection and configuration remain future integration decisions.

## Later-increment boundary

- **Increment 2 (`v0.2.0-design` / `v0.2.0`):** Event Management & Exploration (UC03, UC04; FR-05–FR-10).
- **Increment 3 (`v0.3.0-design` / `v0.3.0`):** Applications, Tasks & Attendance (UC05, UC06; FR-11–FR-18).
- **Increment 4 (`v0.4.0-design` / `v0.4.0`):** Statistics & Analytics (UC07; FR-19, FR-21).

## Diagram sources and rendering

Finalized Increment 1 PlantUML sources:

- `uml/use_case.puml`
- `uml/class_diagram.puml`
- `uml/sequence-diagrams/SD01_High_Level_UC01_Auth.puml`
- `uml/sequence-diagrams/SD02_High_Level_UC02_UserManagement.puml`
- `uml/sequence-diagrams/SD03_Low_Level_UC01_Auth.puml`
- `uml/sequence-diagrams/SD04_Low_Level_UC02_UserManagement.puml`
- `uml/activity-diagrams/AD_Increment1_Combined.puml`
- `uml/erd_increment1.puml`

From the repository root, with Java and `plantuml.jar` available, render all finalized Increment 1 diagrams into `uml/rendered/` with one command:

```powershell
java -jar plantuml.jar -tpng -o rendered uml/use_case.puml uml/class_diagram.puml uml/sequence-diagrams/SD01_High_Level_UC01_Auth.puml uml/sequence-diagrams/SD02_High_Level_UC02_UserManagement.puml uml/sequence-diagrams/SD03_Low_Level_UC01_Auth.puml uml/sequence-diagrams/SD04_Low_Level_UC02_UserManagement.puml uml/activity-diagrams/AD_Increment1_Combined.puml uml/erd_increment1.puml
```

The generated PNGs are diagram renders, not evidence of working application behavior.
