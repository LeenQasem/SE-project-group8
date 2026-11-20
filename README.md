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

```text
src/database/
├── README.md                 # Database scope, setup, and verification notes
├── schema.sql                # Increment 1 MySQL Role and User tables
├── seed.sql                  # Three role reference records
├── operations.sql            # Parameterized SQL examples for user management
└── tests/
    └── increment_1_smoke.sql # Schema and role-seed smoke check
```

## 10.4.1 Database (Increment 1)

The project documentation selects **MySQL**. The current database implementation targets MySQL 8.0.16 or newer with InnoDB; it uses plain SQL scripts, with no ORM or application database driver currently included. The initial schema supports Increment 1 authentication and user management through two tables: `Role` and `User`. Each user has one required role. Primary and foreign keys, unique role names and emails, required fields, role-value checks, and restricted role deletion protect data integrity.

The role seed inserts Administrator, Event Organizer, and Volunteer. The registration SQL example assigns Volunteer. No user accounts or passwords are seeded. The database stores a `password_hash`; password hashing, authentication, session handling, and role authorization require backend code, which is not yet present in this repository. Events, applications, tasks, attendance, and reports belong to later increments and are not in this schema.

### Set up the database

Install MySQL Server and the MySQL command-line client, version 8.0.16 or newer. In PowerShell, create the development database and load the schema and role seed:

```powershell
mysql -u root -p -e "CREATE DATABASE evms CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"
Get-Content -Raw src/database/schema.sql | mysql -u root -p evms
Get-Content -Raw src/database/seed.sql | mysql -u root -p evms
```

The SQL files do not require environment variables. The repository has no application connection configuration yet; do not commit database credentials when backend configuration is added. The schema can be reapplied with `CREATE TABLE IF NOT EXISTS`, and the role seed is repeatable.

### Verify the database

The existing smoke check requires a separate, disposable test database. Create and initialize it, then run the check:

```powershell
mysql -u root -p -e "CREATE DATABASE evms_test CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"
Get-Content -Raw src/database/schema.sql | mysql -u root -p evms_test
Get-Content -Raw src/database/seed.sql | mysql -u root -p evms_test
Get-Content -Raw src/database/tests/increment_1_smoke.sql | mysql -u root -p evms_test
```

The smoke script verifies that the two tables exist and the three role rows are seeded. It requires permission to create and drop a stored procedure. Additional constraint checks are listed as manual checks in the SQL script; CRUD behavior and persistence across reconnects are not covered by automated tests. A MySQL server/client is required to execute these commands.

See the [database-specific documentation](src/database/README.md) for schema details, data-operation guidance, limitations, and future-increment notes.


---

## 10.5 Incremental Development

The project evolves as one system across four increments. The current database supports Increment 1; later increments are planned to extend this same database rather than create separate systems. Later-increment database features are not implemented yet. See [the incremental development plan](docs/incremental_development_plan.md) for the versioned increments, design and working checkpoints, acceptance criteria, and release process.

---

## 10.6 Contributions

 Layan ALqardahji: Responsible for identifying and designing the system architecture and the class diagram.
 Leen Qasem: Responsible for defining and documenting the non-functional requirements, as well as creating the Use Case Diagram .
 Layan Sanabrah: Responsible for gathering and documenting the functional requirements, as well as creating the Sequence Diagram.
 Layan Abu Salah: The Activity Diagram and Database Diagram.

---

**Architecture update:** The three-tier React / Node.js-Express / MySQL design integrates with an Email Service for registration/verification and application status messages (FR-01, FR-12), and Cloud Backup Storage for daily offsite MySQL backups with 30-day retention and recovery support (NFR-03, NFR-06, NFR-07). See `docs/architecture.md`, `docs/traceability_matrix.md`, and the C4 diagrams under `uml/`.
C4 Deployment View: see uml/deployment.puml, rendered as uml/rendered/deployment.png, and documented in docs/architecture.md (Section 5.1).
