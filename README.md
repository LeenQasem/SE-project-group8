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
* **Main Technologies & Tools:** HTML, CSS, JavaScript,react, Node.js, MySQL, Git & GitHub, Draw.io.

---

## 10.3 Architecture and Diagrams
* **System Architecture Diagram:** Illustrates the high-level client-server structure, routing, and database interaction layers.
* **Use Case Diagram:** Maps the functional interactions between Administrators, Event Organizers, and Volunteers across core system modules.
* **Class Diagram:** Defines the domain entities (User, Event, Application, Assignment, Attendance) along with their attributes, methods, and relationships.
* **Sequence Diagrams:** Details step-by-step object interactions for key workflows including volunteer registration, application approval, and attendance logging.
* **Entity-Relationship (ER) Diagram:** Models the relational database schema, primary/foreign keys, and data integrity constraints.

---

## 10.4 Repository Structure
* `/database` â€” Stores database schema definitions, migration scripts, and initial seed data.


---

## 10.5 Incremental Development

---

## 10.6 Contributions

â€¢ Layan ALqardahji: Responsible for identifying and designing the system architecture and the class diagram.
â€¢ Leen Qasem: Responsible for defining and documenting the non-functional requirements, as well as creating the Use Case Diagram .
â€¢ Layan Sanabrah: Responsible for gathering and documenting the functional requirements, as well as creating the Sequence Diagram.
â€¢ Layan Abu Salah: The Activity Diagram and Database Diagram.

---

**Architecture update:** The three-tier React / Node.js-Express / MySQL design integrates with an Email Service for registration/verification and application status messages (FR-01, FR-12), and Cloud Backup Storage for daily offsite MySQL backups with 30-day retention and recovery support (NFR-03, NFR-06, NFR-07). See `docs/architecture.md`, `docs/traceability_matrix.md`, and the C4 diagrams under `uml/`.