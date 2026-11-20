# Increment 1 Requirements Traceability (v0.1.0)

This design maps the supplied requirements to the v0.1.0 scope only. `docs/requirements.md` defines FR-01 through FR-21 (there are no FR-22/FR-23); NFR-22 and NFR-23 are non-functional requirements. FR-05–FR-19 and FR-21 are deferred to Increment 2 except where noted as future role boundaries. This matrix is design coverage, not implementation or test evidence.

## Functional requirements

| Requirement | Increment 1 mapping | Models / classes | Status |
|---|---|---|---|
| FR-01 Create account | UC01; `sequence_auth.mmd` | AuthController, AuthService, UserRepository, User, UserRole, `users` | In scope; unique email and salted hash; public role fixed to VOLUNTEER |
| FR-02 Login/logout | UC01; `sequence_auth.mmd` | AuthController, AuthService, UserRepository, UserSession, `user_sessions` | In scope; persisted session expiry and revocation |
| FR-03 User roles | UC01/UC02; `sequence_admin_rbac.mmd` | User, UserRole, UserManagementService, AccessControlService | In scope; administrator-only role changes |
| FR-04 RBAC | UC01/UC02; auth and admin sequences | AccessControlService, UserSession, UserRole, both controllers | In scope; backend authorization |
| FR-05 Create events | UC03 | — | Increment 2 deferred |
| FR-06 Edit/cancel events | UC03 | — | Increment 2 deferred |
| FR-07 Browse events | UC04 | — | Increment 2 deferred |
| FR-08 Search events | UC04 | — | Increment 2 deferred |
| FR-09 View event details | UC04 | — | Increment 2 deferred |
| FR-10 Apply for events | UC04 | — | Increment 2 deferred |
| FR-11 View event applications | UC05 | — | Increment 2 deferred |
| FR-12 Approve/reject applications | UC05 | — | Increment 2 deferred |
| FR-13 View application status | UC06 | — | Increment 2 deferred |
| FR-14 Assign volunteer tasks | UC05 | — | Increment 2 deferred |
| FR-15 View assigned tasks | UC06 | — | Increment 2 deferred |
| FR-16 Record attendance | UC06 | — | Increment 2 deferred |
| FR-17 Calculate volunteer hours | UC06 | — | Increment 2 deferred |
| FR-18 View attendance/hours | UC06 | — | Increment 2 deferred |
| FR-19 Event statistics | UC07 | — | Increment 2 deferred |
| FR-20 Manage user accounts | UC02; `sequence_admin_rbac.mmd` | AdminUserController, UserManagementService, AccessControlService, UserRepository, User | In scope; list/view/update permitted fields and assign roles |
| FR-21 Platform statistics | UC07 | — | Increment 2 deferred |

No FR-22 or FR-23 entries are defined by the requirements source; the similarly numbered requirements are NFR-22 and NFR-23.

## Non-functional requirements

| Requirement | v0.1.0 relevance | Design mapping |
|---|---|---|
| NFR-01 | Relevant | Login/auth request path; performance target requires runtime measurement. |
| NFR-02 | Persistence/operations | MySQL backup to Cloud Backup Storage at least daily with configured 30-day retention; operational job is not account functionality. |
| NFR-03 | Persistence/operations | Recovery within four hours; restore procedure and recovery evidence required. |
| NFR-04 | Deferred | Concurrency controls for event/application/attendance operations in Increment 2. |
| NFR-05 | Relevant | Generic authentication/admin errors; no internal details exposed. |
| NFR-6 (source label) | Relevant | Source text anomalously says “NFR-6: NFR-10”; confirm intended identifier before claiming coverage. |
| NFR-7–NFR-9 | Mostly deferred | Capacity/scaling and event capacity apply to later workload; deployment architecture remains extensible. |
| NFR-10 | Relevant | Salted one-way password hashing; never persist plaintext. |
| NFR-11 | Relevant | HTTPS/TLS and protected MySQL storage/access. |
| NFR-12 | Relevant | Backend role checks and account/session data isolation. |
| NFR-13 | Relevant | Validate/sanitize registration and account update input. |
| NFR-14 | Relevant | Audit log successful/failed login, authorization denial, account/role changes. |
| NFR-15 | Relevant | Minimize account fields; privacy management constrained to authorized account operations. |
| NFR-16–NFR-18 | Relevant | Responsive UI, consistent role navigation and field-level validation feedback. |
| NFR-19 | Relevant | Four-layer separation: boundary, services, data access, domain. |
| NFR-20 | Relevant | Operational/security logs exclude passwords, tokens, bootstrap secrets. |
| NFR-21 | Relevant | Automated auth and RBAC tests required; none are present in this design-only checkout. |
| NFR-22 | Relevant | Document APIs/schema/deployment/configuration; this design documentation provides a starting point. |
| NFR-23 | Relevant | Browser support verified when frontend is implemented. |
| NFR-24 | Relevant | MySQL/repository boundary and portable deployment configuration. |
| NFR-25 | Later | Event/user time-zone behavior is deferred with event functionality. |

## Diagram index

| Purpose | Editable source |
|---|---|
| Increment 1 / deferred use cases | `uml/use_case.puml` |
| Four-layer class model | `uml/class_diagram.puml` |
| Registration, login, validation, logout | `uml/sequence_auth.mmd` |
| Account management, roles, initial admin guard | `uml/sequence_admin_rbac.mmd` |
| Combined Increment 1 flow | `uml/sequence_diagram.mmd` |
| Registration/session activity | `uml/activity_increment1.puml` |
| Administrator bootstrap and RBAC activity | `uml/activity_admin_rbac.puml` |
| Increment 1 persistence ERD | `uml/erd_increment1.puml` |
| C4 context/container/component/deployment | `uml/system_context.puml`, `uml/container.puml`, `uml/component.puml`, `uml/deployment.puml` |

The planned automated security tests are listed in `docs/testing.md`: forced Volunteer role, backend RBAC, guarded one-time bootstrap, audit logging, and logout invalidation. These tests are specifications only and have not been executed.
