# Project Description

## 1. Project Overview & Purpose

The **Event & Volunteer Management System** is a proposed web-based platform for organizing community and institutional events and coordinating volunteer participation. It provides a shared place for event organizers to publish opportunities, manage volunteer applications, assign responsibilities, and record participation, while volunteers can discover events and follow their involvement.

The system is intended to address coordination problems that arise when event information and volunteer records are managed manually or across separate channels. Centralized event and application records help organizers track applications and decisions, enforce capacity limits, and avoid duplicate or over-capacity participation. Recorded attendance and hours provide a consistent basis for verifying participation and summarizing volunteer contributions.

## 2. Target Users & Roles

The system defines three roles, represented in its requirements and UML model by `UserRole` values `ADMINISTRATOR`, `EVENT_ORGANIZER`, and `VOLUNTEER`. Role-based access control limits each user to the operations permitted for that role.

- **Volunteer:** Browses and searches available events, submits applications, checks application decisions, views assigned tasks, and reviews attendance records and recorded participation hours.
- **Event Organizer:** Creates, edits, and cancels events; sets required volunteer capacity; reviews and approves or rejects applications; assigns tasks to approved volunteers; records attendance and hours; and views participation statistics for events they organize.
- **Administrator:** Manages user accounts and roles, oversees platform activity, and views platform-wide statistics and reports.

## 3. Core System Capabilities (Scope)

The planned system scope comprises the following functional modules:

- **Authentication and role-based access control:** Account registration, login, and logout are associated with the `User` model and `UserRole`. Passwords are to be stored as salted, one-way password hashes rather than plain text. Authorization is enforced for protected operations.
- **Event creation, discovery, and capacity management:** Event Organizers manage `Event` records, including their details, capacity, and `EventStatus`. Volunteers browse or search events that remain open and have capacity. Application and approval workflows enforce the event's volunteer limit.
- **Volunteer application and approval workflow:** A volunteer submits an `Application` for an event. Its `ApplicationStatus` progresses among `PENDING`, `APPROVED`, and `REJECTED` according to organizer decisions and capacity constraints. The backend is designed to request email messages through the external Email Service for registration/verification and application status updates.
- **Task assignment and execution:** Organizers assign a `Task` to a volunteer approved for the relevant event. `TaskStatus` represents assignment progress using `ASSIGNED`, `IN_PROGRESS`, or `COMPLETED`; volunteers can view their assigned tasks.
- **Attendance recording and volunteer hours:** Organizers record `Attendance` for their events. Attendance records include presence and logged hours, which support the calculation of volunteer participation totals and the volunteer's attendance history.
- **Statistics and reporting:** The `Report` model and `ReportType` support event participation statistics, platform statistics, and participation history. Organizers access statistics for their events, while Administrators access platform-wide summaries.

These capabilities describe the intended functional scope. The requirements and diagrams specify system behavior and design; they do not by themselves establish that each feature has been implemented or verified.

## 4. Technical Architecture & Technology Stack

The system is designed as a three-tier web application:

1. **Frontend:** A responsive React single-page application (SPA), using HTML, CSS, and JavaScript, provides role-aware interfaces in desktop, tablet, and mobile browsers. It presents event discovery and details, applications, assignments, attendance information, and reports. The frontend communicates with the backend through JSON API requests over HTTPS.
2. **Backend:** A modular Node.js and Express REST API handles requests, authentication, role authorization, validation, and business rules. Its logical components include API Routes; Authentication & Authorization; User Management; Event Management; Application Management; Task Assignment; Attendance & Hours; Statistics & Reporting; Data Access; Email Notifications; and Scheduled Backup & Recovery. The backend is the integration boundary for persistence and external services.
3. **Database and security:** A MySQL relational database stores users and roles, events, applications, assignments, attendance, hours, and reporting data. It is placed on a private network, with SQL access restricted to the backend. The design calls for HTTPS/TLS to protect data in transit and appropriate encryption or equivalent access controls for sensitive data at rest.

The backend is designed to send account registration/verification and application decision messages through an external **Email Service** over SMTP/TLS or HTTPS. A scheduled process creates automated daily MySQL backups and uploads them over HTTPS to offsite **Cloud Backup Storage**. The intended backup configuration retains data for at least 30 days and supports a four-hour restoration objective following a declared incident. Email and backup providers have not been selected in the design sources.

## 5. Development Methodology & Project Goals

The project is planned for incremental development, with capabilities delivered in successive stages and aligned with the requirements and architecture. Agentic AI workflows are part of the stated development approach. Requirements-to-code-to-test traceability is a project goal, so implemented behavior and its verification can be related back to the documented requirements. The version progression is planned as `v0.x.0-design` -> `v0.x.0` -> `v1.0.0`, moving from design-stage releases through implementation increments toward the first major release.

The overall goal is to deliver a maintainable and secure platform that makes event coordination, volunteer application management, capacity enforcement, task assignment, attendance recording, and participation reporting more consistent and transparent for all three user roles.
