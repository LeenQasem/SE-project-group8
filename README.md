# SE-project-group8

# Event & Volunteer Management System
## 10.1 Group Information
Group Number: 8
Case-Study Title: Event & Volunteer Management System
Course & Instructor: Software Engineer (13477) -Samer ElKababji
Name: Layan Alqardahji           StudentId: 20241109
Name: Layan Sanabrah             StudentId: 20230638
Name: Leen Qasem                 StudentId: 20230105
Name: Layan Abu Salah            StudentId: 20241108

## 10.2 Project Overview
* **System Purpose:** Centralizes event organization and volunteer coordination into one web platform, replacing fragmented tools like spreadsheets, online forms, and messaging apps.
* **Expected Final Outcome:** A functional web application supporting Administrators, Event Organizers, and Volunteers from event creation and registration through task assignment, attendance tracking, and volunteer hour reporting.
* **Main Technologies & Tools:** HTML, CSS, JavaScript, React, Python, MySQL, Git & GitHub, PlantUML.

---

## 10.3 Architecture and Diagrams
* **System Architecture Diagram:** Illustrates the high-level client-server structure, routing, and database interaction layers.
* **Use Case Diagram:** Maps the functional interactions between Administrators, Event Organizers, and Volunteers across core system modules.
* **Class Diagram:** Increment 1 (`v0.1.0-design`) models `User`, `UserRole`, `AuthController`, and `AdminUserController` for UC01–UC02; `Event`, `Application`, `Task`, and `Attendance` are introduced across Increments 2–4.
* **Sequence Diagrams:** Increment 1 (`v0.1.0-design`) covers UC01–UC02 interactions for `User`, `UserRole`, `AuthController`, and `AdminUserController`; `Event`, `Application`, `Task`, and `Attendance` workflows are introduced across Increments 2–4.
* **Activity Diagram:** Illustrates step-by-step user and system swimlane workflows for authentication and role management.
* **Entity-Relationship (ER) Diagram:** Models the relational database schema, primary/foreign keys, and data integrity constraints.

---

## 10.4 Repository Structure
* `/docs` - Requirements, system architecture, incremental development plan, traceability matrix, and AI development log.
* `/uml` - Editable PlantUML (`.puml`) sources and rendered diagram PNGs under `uml/rendered/`.
* `/prompts` - Mandatory task prompt records for AI-assisted increments.
* `/database` - Planned location for database schema definitions, migration scripts, and initial seed data; this folder is not present in the current repository.


---

## 10.5 Incremental Development

See [the incremental development plan](docs/incremental_development_plan.md) for the four versioned increments, design and working checkpoints, acceptance criteria, and release process.

---

## 10.6 Contributions

 Layan ALqardahji: Responsible for identifying and designing the system architecture and the class diagram.
 Leen Qasem: Responsible for defining and documenting the non-functional requirements, as well as creating the Use Case Diagram .
 Layan Sanabrah: Responsible for gathering and documenting the functional requirements, as well as creating the Sequence Diagram.
 Layan Abu Salah: The Activity Diagram and Database Diagram.

---

**Architecture update:** Increment 1 (`v0.1.0-design`) documents the planned three-tier React / Python / MySQL architecture for UC01–UC02. Email Service notifications are deferred to later application increments; email is not part of Increment 1 registration. Backup and recovery are operational requirements; Cloud Backup Storage is not modeled as an Increment 1 integration. See [the architecture](docs/architecture.md), [the incremental development plan](docs/incremental_development_plan.md), [the traceability matrix](docs/traceability_matrix.md), [the AI development log](docs/ai_development_log.md), and the C4 diagrams under `uml/`.
C4 Deployment View: see [uml/deployment.puml](uml/deployment.puml), rendered as [uml/rendered/deployment.png](uml/rendered/deployment.png), and documented in [docs/architecture.md](docs/architecture.md) (Section 5.1).
