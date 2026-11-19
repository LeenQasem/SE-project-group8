# Incremental Development Plan
## Event & Volunteer Management System

### 1. Development Approach

The Event & Volunteer Management System will be developed using an incremental development approach. The system will be divided into four functional increments, each introducing a specific set of related capabilities.

Each increment will have two checkpoints:

- **Design checkpoint (`-design`):** Requirements, workflows, architecture and relevant UML/database designs are prepared and reviewed before implementation.
- **Working checkpoint:** The approved functionality is implemented using Agentic AI, tested, validated and merged through GitHub.

The four increments follow the natural workflow of the system:

1. Authentication and User Management.
2. Event Management and Discovery.
3. Volunteer Applications and Assignments.
4. Attendance, Hours Tracking and Reports.

After completing all four increments, the team will integrate and validate the complete application before releasing version `v1.0.0`.

---

### 2. Increment Summary

| Version | Type | Capability / Scope | Deliverables / Evidence | Requirements / Design Links |
|---|---|---|---|---|
| `v0.1.0-design` | Design | Authentication and User Management | Authentication workflow, role permissions, initial ERD | FR-01-FR-04, FR-20; NFR-01, NFR-05, NFR-10-NFR-15, NFR-17-NFR-22 |
| `v0.1.0` | Working | User registration, login, logout, account management and role-based access | Authentication module, user management module, automated tests | FR-01-FR-04, FR-20; NFR-01, NFR-05, NFR-10-NFR-15, NFR-17-NFR-22 |
| `v0.2.0-design` | Design | Event Management and Discovery | Event workflows, event data model and updated ERD | FR-05-FR-09; NFR-05, NFR-11-NFR-13, NFR-16-NFR-20, NFR-22-NFR-25 |
| `v0.2.0` | Working | Event creation, editing, cancellation, browsing and searching | Event management module, event discovery module, automated tests | FR-05-FR-09; NFR-05, NFR-11-NFR-13, NFR-16-NFR-25 |
| `v0.3.0-design` | Design | Volunteer Applications and Assignments | Application workflows, approval process, assignment workflow and updated ERD | FR-10-FR-15; NFR-01, NFR-04-NFR-07, NFR-09, NFR-11-NFR-15, NFR-18, NFR-20-NFR-22, NFR-25 |
| `v0.3.0` | Working | Application submission, approval, rejection, status tracking and task assignment | Application module, assignment module, automated tests | FR-10-FR-15; NFR-01, NFR-04-NFR-07, NFR-09, NFR-11-NFR-15, NFR-18, NFR-20-NFR-22, NFR-25 |
| `v0.4.0-design` | Design | Attendance, Hours Tracking and Reports | Attendance workflow, hours calculation rules, reporting design and updated ERD | FR-16-FR-19, FR-21; NFR-01, NFR-03-NFR-05, NFR-11-NFR-15, NFR-20-NFR-22, NFR-25 |
| `v0.4.0` | Working | Attendance recording, volunteer-hours calculation, participation history and reports | Attendance module, hours-tracking module, reporting module and automated tests | FR-16-FR-19, FR-21; NFR-01, NFR-03-NFR-05, NFR-11-NFR-15, NFR-20-NFR-22, NFR-25 |
| `v1.0.0` | Final | Complete Integrated System | Integrated application, system testing, final documentation and demonstration | FR-01-FR-21; NFR-01-NFR-25, including NFR-6 (500 concurrent active users; shown as NFR-6: NFR-10 in requirements); complete UML and architecture documentation |

---

### 3. Detailed Increment Specifications

## Increment 1: Authentication and User Management

**Versions:** `v0.1.0-design` → `v0.1.0`

**Objective:**

Establish the foundation of the system by implementing user authentication, account management and role-based access control.

#### Design checkpoint: v0.1.0-design

**Main question:**

How will users register, log in and access the system according to their assigned roles and permissions?

**Scope:**
- Define the Administrator, Event Organizer and Volunteer roles.
- Define user account creation and login workflows, including volunteer registration.
- Define user authentication and credential validation.
- Specify role-based access permissions.
- Define administrator management of user and organizer accounts.
- Design the initial database structure for users and roles.

**Tools:**
- PlantUML for UML diagrams.
- Database modeling tools for the ERD.
- Markdown for requirements and design documentation.
- GitHub for version control.

**Deliverables:**
- Authentication Activity Diagram.
- Initial Entity Relationship Diagram.
- User-role and permission specifications.
- Updated requirements documentation.

**Acceptance criteria:**
- All three user roles are clearly defined.
- Registration and login workflows are documented.
- Role permissions are specified.
- User and Role entities and their relationships are represented in the ERD.
- The design is reviewed and approved by the team.

#### Working checkpoint: v0.1.0

**Main question:**

Can users securely access the system and receive permissions according to their assigned roles?

**Scope:**
- Implement user account creation, including volunteer registration, according to the approved role-assignment design.
- Implement login and logout.
- Validate user credentials.
- Store passwords securely.
- Implement role-based access control.
- Allow administrators to manage user and organizer accounts.

**Tools:**
- Agentic AI coding tool (Codex or another approved agent).
- Git and GitHub.
- The team's selected frontend, backend and database technologies.
- Appropriate automated testing tools.

**Deliverables:**
- Functional authentication module.
- User and role management functionality.
- Role-based access control.
- Automated test results.
- Updated technical documentation.

**Acceptance criteria:**
- Users can create accounts using valid information according to the approved role-assignment design.
- Users can log in and log out.
- Invalid credentials are rejected.
- Passwords are stored securely.
- Users can access only the functionality permitted by their roles.
- Administrators can manage user and organizer accounts.
- Relevant automated tests pass.

---

## Increment 2: Event Management and Discovery

**Versions:** `v0.2.0-design` → `v0.2.0`

**Objective:**

Enable event organizers to create and manage events while allowing volunteers to browse and search for available volunteering opportunities.

#### Design checkpoint: v0.2.0-design

**Main question:**

How will organizers create and manage events, and how will volunteers discover available events?

**Scope:**
- Define event information and attributes.
- Design event creation and editing workflows.
- Define event cancellation rules.
- Design event browsing and searching.
- Define the relationship between events and their organizers.
- Update the ERD to include the Event entity.

**Tools:**
- PlantUML or draw.io.
- Database modeling tools.
- Markdown documentation.
- GitHub.

**Deliverables:**
- Event management workflow diagrams.
- Updated ERD.
- Event management specifications.
- Updated requirements documentation.

**Acceptance criteria:**
- Event attributes are identified.
- Event creation, editing and cancellation workflows are documented.
- The relationship between organizers and events is defined.
- Event discovery and searching workflows are documented.
- The design is consistent with the first increment.

#### Working checkpoint: v0.2.0

**Main question:**

Can organizers manage events while volunteers can browse and search for available opportunities?

**Scope:**
- Implement event creation.
- Implement event editing.
- Implement event cancellation.
- Allow volunteers to browse available events.
- Implement event searching.
- Display event details.
- Integrate event functionality with authentication and role permissions.

**Tools:**
- Agentic AI coding tool.
- Git and GitHub.
- Selected application technologies.
- Automated testing tools.

**Deliverables:**
- Functional event management module.
- Event browsing and searching functionality.
- Updated database schema.
- Automated test results.
- Updated technical documentation.

**Acceptance criteria:**
- Authorized organizers can create events.
- Organizers can edit and cancel their events.
- Volunteers can browse available events.
- Volunteers can search for events.
- Unauthorized users cannot perform organizer-only operations.
- Event information is stored and retrieved correctly.
- Relevant automated tests pass.

---

## Increment 3: Volunteer Applications and Assignments

**Versions:** `v0.3.0-design` → `v0.3.0`

**Objective:**

Allow volunteers to apply for events and enable organizers to review applications, make approval decisions and assign tasks and responsibilities to approved volunteers.

#### Design checkpoint: v0.3.0-design

**Main question:**

How will volunteers apply to events, how will organizers process applications, and how will approved volunteers receive assignments?

**Scope:**
- Define the volunteer application process.
- Define application statuses: Pending, Approved and Rejected.
- Design the application review and approval workflow.
- Define event capacity enforcement during approval.
- Design task and responsibility assignment workflows.
- Update the ERD to include Application and Task entities and their relationships.

**Tools:**
- PlantUML.
- Database modeling tools.
- Markdown documentation.
- GitHub.

**Deliverables:**
- Application workflow diagrams.
- Assignment workflow diagrams.
- Updated ERD.
- Application status specifications.
- Updated requirements documentation.

**Acceptance criteria:**
- Application submission and review processes are documented.
- Application statuses and their transitions are defined.
- Event capacity rules are documented.
- Task assignment rules are defined.
- Relationships between volunteers, events, applications and tasks are represented in the ERD.
- The design is reviewed and approved.

#### Working checkpoint: v0.3.0

**Main question:**

Can volunteers apply to events, can organizers process applications, and can approved volunteers receive assigned tasks?

**Scope:**
- Implement volunteer application submission.
- Allow volunteers to view their applications.
- Allow organizers to review applications.
- Implement application approval and rejection.
- Update application status.
- Enforce event capacity when approving applications.
- Allow organizers to assign tasks to approved volunteers.
- Allow volunteers to view their assigned tasks.

**Tools:**
- Agentic AI coding tool.
- Git and GitHub.
- Selected application technologies.
- Automated testing tools.

**Deliverables:**
- Functional application management module.
- Application status tracking.
- Event capacity enforcement.
- Task assignment functionality.
- Updated database schema.
- Automated test results.
- Updated technical documentation.

**Acceptance criteria:**
- Volunteers can apply to available events.
- Organizers can view applications for their events.
- Organizers can approve or reject applications.
- Application statuses are updated correctly.
- Event capacity cannot be exceeded through application approval.
- Only approved volunteers can receive task assignments.
- Volunteers can view their assigned tasks.
- Relevant automated tests pass.

---

## Increment 4: Attendance, Hours Tracking and Reports

**Versions:** `v0.4.0-design` → `v0.4.0`

**Objective:**

Complete the main volunteer participation process by recording attendance, calculating volunteer participation hours and providing participation reports and platform statistics.

#### Design checkpoint: v0.4.0-design

**Main question:**

How will the system record volunteer attendance, calculate volunteer participation hours and generate participation reports?

**Scope:**
- Define attendance recording requirements.
- Design the attendance recording workflow.
- Define how attendance relates to volunteers and events.
- Specify the volunteer-hours calculation rules.
- Design volunteer participation history.
- Define event participation reporting.
- Define administrator platform statistics.
- Update the ERD to include Attendance and any required data structures.

**Tools:**
- PlantUML.
- Database modeling tools.
- Markdown documentation.
- GitHub.

**Deliverables:**
- Attendance workflow diagram.
- Volunteer-hours calculation specifications.
- Updated ERD.
- Reporting and statistics specifications.
- Updated requirements documentation.

**Acceptance criteria:**
- Attendance recording rules are documented.
- The volunteer-hours calculation method is defined.
- Attendance records are associated with the correct volunteers and events.
- Reporting requirements for organizers and administrators are specified.
- The design is consistent with the previous increments.
- The design is reviewed and approved.

#### Working checkpoint: v0.4.0

**Main question:**

Can the system accurately record attendance, calculate volunteer hours and provide useful participation reports?

**Scope:**
- Implement attendance recording by organizers.
- Store volunteer attendance records.
- Calculate volunteer participation hours according to the agreed rules.
- Allow volunteers to view accumulated hours.
- Display volunteer participation history.
- Generate event participation reports for organizers.
- Provide overall platform statistics for administrators.

**Tools:**
- Agentic AI coding tool.
- Git and GitHub.
- Selected application technologies.
- Automated testing tools.

**Deliverables:**
- Functional attendance module.
- Volunteer-hours tracking functionality.
- Volunteer participation history.
- Event participation reports.
- Administrator statistics.
- Automated test results.
- Updated technical documentation.

**Acceptance criteria:**
- Organizers can record volunteer attendance.
- Attendance records are stored correctly.
- Volunteer hours are calculated according to the agreed rules.
- Volunteers can view their accumulated hours and participation history.
- Organizers can view event participation reports.
- Administrators can view overall platform statistics.
- Relevant automated tests pass.

---

### 4. Final Integration and Release

**Version:** `v1.0.0`

After completing the four increments, the team will integrate and validate the complete application.

**Main question:**

Do all implemented modules work together correctly to support the complete Event & Volunteer Management System workflow?

**Tools:**
- Git and GitHub.
- Agentic AI coding tool.
- Automated testing tools.
- Markdown documentation.

**Activities:**
- Integrate all four increments.
- Verify authentication and role permissions across all modules.
- Test the complete volunteer journey, from registration and event discovery to application, assignment, attendance and hours tracking.
- Test organizer and administrator workflows.
- Perform integration and system testing.
- Fix identified defects.
- Review and finalize UML diagrams and database documentation.
- Finalize project documentation and prepare the final demonstration.

**Deliverables:**
- Fully integrated application.
- Complete and updated UML diagrams.
- Final database schema.
- System and integration test results.
- Updated AI development log.
- Updated traceability matrix.
- Final README and technical documentation.
- Final project report and demonstration.

**Acceptance criteria:**
- All applicable functional and non-functional requirements are implemented and validated.
- All three user roles can perform their authorized operations.
- All four increments work together correctly.
- Critical user workflows pass system testing.
- No critical unresolved defects remain.
- Documentation and diagrams reflect the final implementation.
- The system is ready for final demonstration.

---

### 5. Development and Version Control Process

The following process will be followed for every increment:

1. Review and finalize the requirements for the selected increment.
2. Prepare the relevant architecture, UML and database designs.
3. Review and approve the design checkpoint.
4. Merge the reviewed design work and create its `-design` version tag.
5. Use an Agentic AI coding tool to implement the approved functionality.
6. Review the AI-generated code and verify its consistency with the design.
7. Generate and execute appropriate automated tests.
8. Correct identified implementation or testing issues.
9. Open a GitHub pull request for review.
10. Merge the completed increment into the integration branch.
11. Create the working-version tag on the reviewed and merged commit.
12. Update the AI development log, traceability matrix, testing documentation and relevant diagrams.

All meaningful Agentic AI tasks will be documented in the `/prompts/` directory using Markdown files. The team will maintain `/docs/ai_development_log.md` and `/docs/traceability_matrix.md` throughout development.

### 6. Final Release

The final release, `v1.0.0`, will represent the completed, integrated, tested and documented Event & Volunteer Management System.

