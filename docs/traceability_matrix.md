# Requirements Traceability Matrix — Event & Volunteer Management System

This matrix follows the four-increment roadmap in [the development plan](incremental_development_plan.md). Working versions and test paths are planned unless marked as design evidence; this repository does not yet contain application modules or automated test files. The Increment 1 ERD models `User` and the `users.role` enum column; it does not define a separate `Role` table.

## Functional Requirements (FR-01–FR-21)

| Requirement ID | Use Case / Design Element | Increment / Version | Implementation Module(s) | Test(s) | Status |
|---|---|---|---|---|---|
| FR-01 | UC01; `AuthController`, `User`, `UserRole`; [SD01](../uml/sequence-diagrams/SD01_High_Level_UC01_Auth.puml), [SD03](../uml/sequence-diagrams/SD03_Low_Level_UC01_Auth.puml), [combined activity](../uml/activity-diagrams/AD_Increment1_Combined.puml), [ERD: User and role enum](../uml/erd_increment1.puml) | Increment 1 (`v0.1.0-design` / `v0.1.0`) | Planned: `AuthController`, `User` | Planned: `tests/auth/register.test.js` | Designed (`v0.1.0-design`) |
| FR-02 | UC01; `AuthController`, `User`; [SD01](../uml/sequence-diagrams/SD01_High_Level_UC01_Auth.puml), [SD03](../uml/sequence-diagrams/SD03_Low_Level_UC01_Auth.puml), [combined activity](../uml/activity-diagrams/AD_Increment1_Combined.puml) | Increment 1 (`v0.1.0-design` / `v0.1.0`) | Planned: `AuthController`, `User` | Planned: `tests/auth/login_logout.test.js` | Designed (`v0.1.0-design`) |
| FR-03 | UC01, UC02; `User`, `UserRole`, `AdminUserController`; [SD02](../uml/sequence-diagrams/SD02_High_Level_UC02_UserManagement.puml), [SD04](../uml/sequence-diagrams/SD04_Low_Level_UC02_UserManagement.puml), [ERD role enum](../uml/erd_increment1.puml) | Increment 1 (`v0.1.0-design` / `v0.1.0`) | Planned: `AdminUserController`, `User`, `UserRole` | Planned: `tests/admin/roles.test.js` | Designed (`v0.1.0-design`) |
| FR-04 | UC01, UC02; `User.hasRole()`, `AuthController`, `AdminUserController`; [SD03](../uml/sequence-diagrams/SD03_Low_Level_UC01_Auth.puml), [SD04](../uml/sequence-diagrams/SD04_Low_Level_UC02_UserManagement.puml) | Increment 1 (`v0.1.0-design` / `v0.1.0`) | Planned: `AuthController`, `AdminUserController`, `User` | Planned: `tests/auth/rbac.test.js` | Designed (`v0.1.0-design`) |
| FR-05–FR-06 | UC03; planned Increment 2 UML under `uml/increment2/` | Increment 2 (`v0.2.0-design` / `v0.2.0`) | Planned: Event module | Planned: `tests/events/` | Deferred to Increment 2 |
| FR-07–FR-10 | UC04; planned Increment 2 UML under `uml/increment2/` | Increment 2 (`v0.2.0-design` / `v0.2.0`) | Planned: Explore module | Planned: `tests/explore/` | Deferred to Increment 2 |
| FR-11, FR-12, FR-14 | UC05; planned Increment 3 UML under `uml/increment3/` | Increment 3 (`v0.3.0-design` / `v0.3.0`) | Planned: Application module | Planned: `tests/applications/` | Deferred to Increment 3 |
| FR-13, FR-15–FR-18 | UC06; planned Increment 3 UML under `uml/increment3/` | Increment 3 (`v0.3.0-design` / `v0.3.0`) | Planned: Attendance module | Planned: `tests/attendance/` | Deferred to Increment 3 |
| FR-20 | UC02; `AdminUserController`, `User`, `UserRole`; [SD02](../uml/sequence-diagrams/SD02_High_Level_UC02_UserManagement.puml), [SD04](../uml/sequence-diagrams/SD04_Low_Level_UC02_UserManagement.puml), [combined activity](../uml/activity-diagrams/AD_Increment1_Combined.puml), [ERD](../uml/erd_increment1.puml) | Increment 1 (`v0.1.0-design` / `v0.1.0`) | Planned: `AdminUserController`, `User` | Planned: `tests/admin/user_management.test.js` | Designed (`v0.1.0-design`) |
| FR-19, FR-21 | UC07; planned Increment 4 UML under `uml/increment4/` | Increment 4 (`v0.4.0-design` / `v0.4.0`) | Planned: Analytics module | Planned: `tests/analytics/` | Deferred to Increment 4 |

FR-01 registration uses a salted one-way password hash and assigns `VOLUNTEER` server-side by default. Public registration cannot assign privileged roles. The first Administrator is provisioned manually through a guarded setup; subsequent role assignment is administrator-only.

## Non-Functional Requirements (NFR-01–NFR-25)

| Requirement ID | Increment 1 design mapping | Planned verification | Status |
|---|---|---|---|
| NFR-01 | UC01 login flow; `AuthController` | Login latency measurement against requirement target | Verify with implementation |
| NFR-02 | MySQL persistence and backup operations | Backup/retention configuration check | Operational; verify at deployment |
| NFR-03 | Persistence recovery documentation | Restore/recovery exercise | Operational; verify at deployment |
| NFR-04 | Later event/application concurrency | Concurrency tests in later increments | Deferred with affected workflows |
| NFR-05 | UC01/UC02 safe errors | Auth/admin error-response tests | Planned |
| NFR-6* | Platform capacity; source label is malformed | Load test when deployed | Verify; confirm source identifier |
| NFR-7 | System growth | Scale/data-volume tests | Planned for integration |
| NFR-8 | Layerable deployment design | Horizontal scaling test | Planned for deployment |
| NFR-9 | Later event capacity | Event capacity tests | Deferred to Increment 2 |
| NFR-10 | `User.passwordHash`; `AuthController.register()` | Verify salted one-way hashing and no plaintext persistence | Planned: `tests/auth/register.test.js` |
| NFR-11 | HTTPS and protected database deployment | Transport/storage security review | Planned for deployment |
| NFR-12 | UC01/UC02 role checks; `User.hasRole()` | Reject unauthenticated/non-admin protected requests | Planned: `tests/auth/rbac.test.js` |
| NFR-13 | Registration and account-update inputs | Invalid/malicious input tests | Planned: auth/admin test suites |
| NFR-14 | Account/login security events | Audit-event coverage tests | Planned |
| NFR-15 | Minimal `User` attributes and authorized account management | Data-minimization/access review | Planned |
| NFR-16 | React UI | Responsive viewport checks | Planned for frontend |
| NFR-17 | Shared role terminology and feedback | UI consistency review | Planned for frontend |
| NFR-18 | Registration/admin forms | Field-level validation tests | Planned: auth/admin test suites |
| NFR-19 | Controller-to-entity design separation | UML/code responsibility review | Designed; verify against implementation |
| NFR-20 | Secret-safe logging policy | Log inspection tests | Planned |
| NFR-21 | Critical workflow automation | Auth/RBAC automated test suite | Planned: `tests/auth/`, `tests/admin/` |
| NFR-22 | This plan, architecture and UML artifacts | Documentation link/completeness review | Design documentation |
| NFR-23 | Supported browser requirement | Browser compatibility checks | Planned for frontend |
| NFR-24 | MySQL and data-access portability | Migration/restore portability exercise | Planned for deployment |
| NFR-25 | Event/user time-zone behavior | Date/time integration tests | Deferred with event features |

\* `docs/requirements.md` labels the 500-concurrent-user requirement `NFR-6: NFR-10`. This matrix preserves `NFR-6` as the visible source label and flags it for clarification; NFR-10 remains the separate password-hashing requirement.

## Design-to-Code Synchronization Rule

If implementation changes class responsibilities, interfaces, or workflows, the corresponding UML artifacts under `uml/` will be updated before tagging the working release.

## Increment 1 Diagram Index

- [Use Case Diagram](../uml/use_case.puml)
- [Class Diagram](../uml/class_diagram.puml)
- [SD01 — High-Level UC01 Authentication](../uml/sequence-diagrams/SD01_High_Level_UC01_Auth.puml)
- [SD02 — High-Level UC02 User Management](../uml/sequence-diagrams/SD02_High_Level_UC02_UserManagement.puml)
- [SD03 — Low-Level UC01 Authentication](../uml/sequence-diagrams/SD03_Low_Level_UC01_Auth.puml)
- [SD04 — Low-Level UC02 User Management](../uml/sequence-diagrams/SD04_Low_Level_UC02_UserManagement.puml)
- [Combined UC01/UC02 Activity Diagram](../uml/activity-diagrams/AD_Increment1_Combined.puml)
- [Increment 1 ERD](../uml/erd_increment1.puml)
