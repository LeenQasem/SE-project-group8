# Incremental Development Plan

## Four-Increment Roadmap

The roadmap separates design milestones (`-design`) from working releases. UC01 and UC02 are Increment 1; UC03–UC04 are Increment 2; UC05–UC06 are Increment 3; UC07 is Increment 4. The simplified Increment 1 feature diagrams are available; later-increment UML, application source, test directories, and working releases remain planned deliverables.

| Version | Type | Capability / Scope | Deliverable / Evidence | Requirements / Design Links |
|---|---|---|---|---|
| v0.1.0-design | Design | User Account, Authentication & RBAC (UC01, UC02) | Simplified UML, traceability | [FR-01–FR-04, FR-20](requirements.md); [use case](../uml/use_case.puml), [class](../uml/class_diagram.puml), [SD01](../uml/sequence-diagrams/SD01_High_Level_UC01_Auth.puml), [SD02](../uml/sequence-diagrams/SD02_High_Level_UC02_UserManagement.puml), [SD03](../uml/sequence-diagrams/SD03_Low_Level_UC01_Auth.puml), [SD04](../uml/sequence-diagrams/SD04_Low_Level_UC02_UserManagement.puml), [combined activity](../uml/activity-diagrams/AD_Increment1_Combined.puml), [initial ERD](../uml/erd_increment1.puml), [traceability](traceability_matrix.md) |
| v0.1.0 | Working | User Account, Authentication & RBAC (UC01, UC02) | Working code, tests, demo | [FR-01–FR-04, FR-20](requirements.md); planned tests: `tests/auth/`, `tests/admin/`; [test plan](testing.md) |
| v0.2.0-design | Design | Event Management & Exploration (UC03, UC04) | Updated UML and events/applications ERD | [FR-05–FR-10](requirements.md); planned diagrams: `uml/increment2/use_case.puml`, `uml/increment2/class_diagram.puml`, `uml/increment2/erd.puml`, `uml/increment2/sequence_*.puml` |
| v0.2.0 | Working | Event Management & Exploration (UC03, UC04) | Event/browse/apply code, tests, demo | [FR-05–FR-10](requirements.md); planned modules: Event and Explore; tests: `tests/events/`, `tests/explore/` |
| v0.3.0-design | Design | Applications, Tasks & Attendance (UC05, UC06) | Updated UML and tasks/attendance ERD | [FR-11–FR-18](requirements.md); planned diagrams: `uml/increment3/use_case.puml`, `uml/increment3/class_diagram.puml`, `uml/increment3/erd.puml`, `uml/increment3/sequence_*.puml` |
| v0.3.0 | Working | Applications, Tasks & Attendance (UC05, UC06) | Approval/task/hours code, tests, demo | [FR-11–FR-18](requirements.md); planned modules: Application and Attendance; tests: `tests/applications/`, `tests/attendance/` |
| v0.4.0-design | Design | Statistics & Analytics (UC07) | Updated metrics UML | [FR-19, FR-21](requirements.md); planned diagrams: `uml/increment4/use_case.puml`, `uml/increment4/class_diagram.puml`, `uml/increment4/sequence_*.puml` |
| v0.4.0 | Working | Statistics & Analytics (UC07) | Reporting/statistics code, tests, demo | [FR-19, FR-21](requirements.md); planned module: Analytics; tests: `tests/analytics/` |
| v1.0.0 | Final Integration | Full Event & Volunteer Management System | Integrated code, full test suite, release demo | [FR-01–FR-21](requirements.md); all modules; `tests/e2e/` |

## Version Acceptance Criteria

### v0.1.0-design — User Account, Authentication & RBAC design

**Main Question:** How do UC01 and UC02 support basic authentication and administrator-only role management with the simplified domain model?

**Tools:** PlantUML, Mermaid CLI for `.mmd` sources, Git/GitHub, Markdown.

**Acceptance Criteria:**

- The Increment 1 class diagram contains only `AuthController`, `AdminUserController`, `User`, and `UserRole` with the specified operations and role enum.
- `AuthController` registration validates input, stores a salted one-way password hash, and assigns `VOLUNTEER` by default; public signup cannot select a privileged role.
- `AdminUserController.assignRole()` is restricted to administrators and accepts only `ADMINISTRATOR`, `EVENT_ORGANIZER`, or `VOLUNTEER`.
- UC01/UC02 sequence and activity diagrams agree with the class/use-case diagrams; the ERD contains only the agreed Increment 1 user persistence fields.
- Design links and FR-01–FR-04/FR-20 traceability are reviewed; diagrams render without PlantUML syntax errors.

### v0.1.0 — User Account, Authentication & RBAC implementation

**Main Question:** Can users register and authenticate safely while only administrators can view accounts and assign roles?

**Tools:** React, Python, MySQL, Git/GitHub, Python standard-library `unittest` runner.

**Acceptance Criteria:**

- Registration, login, and logout are implemented through `AuthController`; users have one valid `UserRole`.
- Passwords are salted and hashed; duplicate/invalid email and invalid credentials are rejected with safe messages.
- New public accounts always receive `VOLUNTEER`; the backend ignores/rejects submitted privileged roles.
- Administrator provisioning is a guarded manual setup; role assignment is administrator-only and validated server-side.
- `tests/auth/` and `tests/admin/` cover registration, hash verification, login/logout, forced default role, authorization, role updates, and provisioning safeguards.
- A demo shows UC01 and UC02; no later-increment workflow is included.

### v0.2.0-design — Event Management & Exploration design

**Main Question:** How can organizers manage events and volunteers discover and apply without exceeding event capacity?

**Tools:** PlantUML, Mermaid CLI, Git/GitHub, Markdown.

**Acceptance Criteria:**

- Planned Increment 2 diagrams define UC03/UC04 and the required event/application persistence.
- FR-05–FR-10 trace to diagrams, domain relationships, and capacity/duplicate checks.
- Deferred diagram sources are kept under `uml/increment2/` and do not alter the v0.1.0 scope.

### v0.2.0 — Event Management & Exploration implementation

**Main Question:** Can organizers publish events and volunteers find and apply to eligible events?

**Tools:** React, Python, MySQL, Git/GitHub, Python standard-library `unittest` runner.

**Acceptance Criteria:**

- Event creation/edit/cancel and event browse/search/details/application flows implement FR-05–FR-10.
- Capacity, event status, and duplicate-application rules are checked by the backend.
- `tests/events/` and `tests/explore/` cover success, invalid input, capacity, and duplicate cases; demo covers UC03/UC04.

### v0.3.0-design — Applications, Tasks & Attendance design

**Main Question:** How do application decisions control task assignment and attendance/hour records?

**Tools:** PlantUML, Mermaid CLI, Git/GitHub, Markdown.

**Acceptance Criteria:**

- Planned Increment 3 UML and ERD cover UC05/UC06 and FR-11–FR-18.
- Approval capacity, approved-volunteer task eligibility, attendance ownership, and hour calculation are explicit.
- Planned diagrams are stored under `uml/increment3/`; earlier increments remain traceable.

### v0.3.0 — Applications, Tasks & Attendance implementation

**Main Question:** Can organizers process applications, assign eligible volunteers, and record participation accurately?

**Tools:** React, Python, MySQL, Git/GitHub, Python standard-library `unittest` runner.

**Acceptance Criteria:**

- Application decisions, task assignment, attendance, and hours implement FR-11–FR-18.
- `tests/applications/` and `tests/attendance/` cover authorization, capacity, eligibility, and non-negative hour calculations.
- Demo covers UC05/UC06 and their validation/error paths.

### v0.4.0-design — Statistics & Analytics design

**Main Question:** Which event and platform metrics must be calculated, and who may view them?

**Tools:** PlantUML, Mermaid CLI, Git/GitHub, Markdown.

**Acceptance Criteria:**

- Planned Increment 4 models cover UC07, FR-19, and FR-21.
- Organizer event metrics and administrator platform metrics have distinct authorization and data scope.
- Planned sources are stored under `uml/increment4/` and map to existing entities from earlier increments.

### v0.4.0 — Statistics & Analytics implementation

**Main Question:** Can authorized organizers and administrators view accurate scoped statistics?

**Tools:** React, Python, MySQL, Git/GitHub, Python standard-library `unittest` runner.

**Acceptance Criteria:**

- Event and platform reports implement FR-19 and FR-21 with correct role and ownership checks.
- `tests/analytics/` verifies metric calculations, filters, and denied access.
- Demo presents event-level and platform-level reporting.

### v1.0.0 — Final Integration

**Main Question:** Do all increments work together as a secure, usable, and traceable system?

**Tools:** React, Python, MySQL, Git/GitHub, Python standard-library `unittest` runner, browser automation selected during implementation, PlantUML/Mermaid.

**Acceptance Criteria:**

- UC01–UC07 and FR-01–FR-21 work across integrated frontend, API, and database layers.
- The complete unit, integration, security, and end-to-end suites pass; `tests/e2e/` covers primary role journeys.
- Release demo, deployment/configuration instructions, final diagrams, and requirement traceability are reviewed.
- Security and performance NFR evidence is recorded; no requirement is marked satisfied without verification.

## Confirmed Increment 1 Role Policy

Public registration always assigns `VOLUNTEER`. The first Administrator is created through guarded manual provisioning. After that bootstrap, only Administrators may assign or change roles. The current simplified Increment 1 class diagram is limited to `AuthController`, `AdminUserController`, `User`, and `UserRole`.
