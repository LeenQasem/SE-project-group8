# Requirements

## 1. Functional Requirements

### 1.1 User Management

**FR-01: Create a User Account**

- **Description:** The system shall allow users to create an account.
- **Input:** Name, email, and password.
- **Process:** The system validates the registration information, checks whether the email is already registered, and saves the new account.
- **Output:** Account creation confirmation.
- **Constraints:** Email must be valid and unique. Passwords must not be stored in plain text.
- **Priority:** High.

**FR-02: User Login and Logout**

- **Description:** The system shall allow registered users to log in and log out.
- **Input:** Email, password, and logout action.
- **Process:** The system verifies the user's credentials and creates or ends the user session.
- **Output:** Login or logout confirmation.
- **Constraints:** Only registered users with valid credentials can log in. Protected features require authentication.
- **Priority:** High.

**FR-03: User Roles Management**

- **Description:** The system shall support three user roles: Administrator, Event Organizer, and Volunteer.
- **Input:** User role information.
- **Process:** The system assigns and stores the appropriate role for each user.
- **Output:** User account with an assigned role.
- **Constraints:** Each user must have one of the three defined roles.
- **Priority:** High.

**FR-04: Role-Based Access Control**

- **Description:** The system shall restrict access to features based on the user's role.
- **Input:** Authenticated user role and requested feature.
- **Process:** The system checks whether the user's role has permission to access the requested feature.
- **Output:** Access granted or denied.
- **Constraints:** Users can only access features permitted for their roles.
- **Priority:** High.

### 1.2 Event Management

**FR-05: Create Events**

- **Description:** The system shall allow Event Organizers to create events.
- **Input:** Event title, description, date, location, and required volunteer capacity.
- **Process:** The system validates the event information and saves the new event.
- **Output:** New event record and creation confirmation.
- **Constraints:** Only Event Organizers can create events. Capacity must be a positive whole number.
- **Priority:** High.

**FR-06: Edit and Cancel Events**

- **Description:** The system shall allow Event Organizers to edit or cancel their events.
- **Input:** Event ID, updated event information, or cancellation action.
- **Process:** The system verifies event ownership and updates or cancels the selected event.
- **Output:** Updated event details or cancellation confirmation.
- **Constraints:** Organizers can only modify their own events. Cancelled events cannot accept new applications.
- **Priority:** High.

**FR-07: Browse Events**

- **Description:** The system shall allow volunteers to browse available events.
- **Input:** Optional browsing criteria.
- **Process:** The system retrieves events that are open for applications and have available volunteer capacity.
- **Output:** List of available events.
- **Constraints:** Cancelled and fully staffed events are excluded.
- **Priority:** High.

**FR-08: Search Events**

- **Description:** The system shall allow volunteers to search for events.
- **Input:** Search text and optional date or location filters.
- **Process:** The system searches event titles, descriptions, dates, and locations based on the entered criteria.
- **Output:** List of matching events.
- **Constraints:** Cancelled and fully staffed events are excluded from search results.
- **Priority:** Medium.

**FR-09: View Event Details**

- **Description:** The system shall display detailed information about selected events.
- **Input:** Event ID.
- **Process:** The system retrieves and displays the selected event information.
- **Output:** Event title, description, date, location, required volunteer capacity, and event status.
- **Constraints:** Only valid event IDs return event details.
- **Priority:** High.

### 1.3 Volunteer Applications

**FR-10: Apply for Events**

- **Description:** The system shall allow volunteers to apply for available events.
- **Input:** Volunteer ID and event ID.
- **Process:** The system checks event availability and whether the volunteer has already applied, then saves the application.
- **Output:** Application confirmation and Pending status.
- **Constraints:** Only volunteers can apply. Duplicate applications are not allowed. Events must not be cancelled or full.
- **Priority:** High.

**FR-11: View Event Applications**

- **Description:** The system shall allow Event Organizers to view applications submitted for their events.
- **Input:** Organizer ID and event ID.
- **Process:** The system retrieves applications associated with the organizer's events.
- **Output:** List of volunteer applications and their statuses.
- **Constraints:** Organizers can only view applications for their own events.
- **Priority:** High.

**FR-12: Approve or Reject Applications**

- **Description:** The system shall allow Event Organizers to approve or reject volunteer applications.
- **Input:** Application ID and approval or rejection decision.
- **Process:** The system verifies event ownership, checks the application status and available capacity, and updates the application status.
- **Output:** Updated application status.
- **Constraints:** Approved volunteers must not exceed the event's required capacity.
- **Priority:** High.

**FR-13: View Application Status**

- **Description:** The system shall allow volunteers to view the status of their applications.
- **Input:** Volunteer account ID.
- **Process:** The system retrieves applications submitted by the volunteer and their current statuses.
- **Output:** List of applications with Pending, Approved, or Rejected statuses.
- **Constraints:** Volunteers can only view their own applications.
- **Priority:** High.

### 1.4 Task Assignment

**FR-14: Assign Tasks to Volunteers**

- **Description:** The system shall allow Event Organizers to assign tasks and responsibilities to approved volunteers.
- **Input:** Event ID, volunteer ID, task name, and task description.
- **Process:** The system verifies the volunteer's approval for the event and saves the task assignment.
- **Output:** Task assignment confirmation and details.
- **Constraints:** Only approved volunteers can receive tasks for the relevant event.
- **Priority:** High.

**FR-15: View Assigned Tasks**

- **Description:** The system shall allow volunteers to view their assigned tasks.
- **Input:** Volunteer account ID.
- **Process:** The system retrieves tasks assigned to the volunteer.
- **Output:** List of assigned tasks and their details.
- **Constraints:** Volunteers can only view their own assigned tasks.
- **Priority:** High.

### 1.5 Attendance and Volunteer Hours

**FR-16: Record Volunteer Attendance**

- **Description:** The system shall allow Event Organizers to record volunteer attendance manually.
- **Input:** Event ID, volunteer ID, and attendance status.
- **Process:** The system verifies the event and volunteer information, then saves the attendance record.
- **Output:** Saved attendance record and confirmation.
- **Constraints:** Only authorized organizers can record attendance for their own events.
- **Priority:** High.

**FR-17: Calculate Volunteer Hours**

- **Description:** The system shall calculate volunteer participation hours based on recorded attendance and entered hours.
- **Input:** Volunteer attendance records and manually entered hours.
- **Process:** The system stores the hours entered by the organizer and calculates the volunteer's total hours across events.
- **Output:** Updated total volunteer hours.
- **Constraints:** Hours must be non-negative. Only valid recorded hours are included.
- **Priority:** High.

**FR-18: View Attendance Records and Total Hours**

- **Description:** The system shall allow volunteers to view their attendance records and total volunteer hours.
- **Input:** Volunteer account ID.
- **Process:** The system retrieves the volunteer's attendance records and total recorded hours.
- **Output:** Attendance history and total volunteer hours.
- **Constraints:** Volunteers can only view their own attendance records and hours.
- **Priority:** High.

### 1.6 Reports and Administration

**FR-19: View Event Participation Statistics**

- **Description:** The system shall allow Event Organizers to view participation statistics for their events.
- **Input:** Organizer ID and event ID.
- **Process:** The system calculates participation statistics using application and attendance records.
- **Output:** Event participation statistics, including application counts, attendance counts, and volunteer hours.
- **Constraints:** Organizers can only view statistics for their own events.
- **Priority:** Medium.

**FR-20: Manage User Accounts**

- **Description:** The system shall allow Administrators to manage user accounts.
- **Input:** User ID and account information or management action.
- **Process:** The system verifies administrator authorization and updates the selected user account.
- **Output:** Updated user account information and confirmation.
- **Constraints:** Only Administrators can manage user accounts.
- **Priority:** High.

**FR-21: View Overall Platform Statistics**

- **Description:** The system shall allow Administrators to view overall platform statistics.
- **Input:** Platform data and optional date filters.
- **Process:** The system aggregates user, event, application, and volunteer-hours data.
- **Output:** Overall platform statistics and summaries.
- **Constraints:** Only Administrators can access platform-wide statistics.
- **Priority:** Medium.

## 2. Non-Functional Requirements

### 2.1 Performance

- **NFR-01:** The system shall complete user login, event registration, volunteer application, and attendance-recording requests within 3 seconds for at least 95% of requests, excluding time spent waiting for external services.

### 2.2 Availability and Reliability

- **NFR-02:** The system shall perform automated backups of application data at least once every 24 hours and retain backups for a minimum of 30 days.
- **NFR-03:** The system shall recover from a service failure and restore normal operation within 4 hours of a declared incident.
- **NFR-04:** The system shall preserve data integrity when concurrent users register for the same event, approve applications, or record attendance.
- **NFR-05:** The system shall display a user-friendly error message when a request fails and shall not expose stack traces, database details, or other internal implementation information.

### 2.3 Scalability and Capacity

- **NFR-6:** NFR-10: The system shall support at least 500 concurrent active users while meeting performance requirements.
- **NFR-7:** The system shall support at least 10,000 registered users, 5,000 events, and 100,000 volunteer applications without requiring changes to core functionality.
- **NFR-8:** The system architecture shall allow application servers and background-processing capacity to be scaled horizontally as user traffic and stored data increase.
- **NFR-9:** The system shall support event registration capacity limits and shall prevent registrations from exceeding the number of volunteers required for an event unless an authorized Event Organizer explicitly changes the limit.

### 2.4 Security and Privacy

- **NFR-10:** The system shall protect passwords using a strong, salted, one-way password-hashing algorithm and shall never store passwords in plain text.
- **NFR-11:** The system shall encrypt sensitive data in transit using HTTPS/TLS and shall protect sensitive data at rest using appropriate encryption or equivalent access controls.
- **NFR-12:** The system shall enforce role-based authorization for every protected operation and shall prevent users from accessing or modifying data belonging to unauthorized users or organizations.
- **NFR-13:** The system shall validate and sanitize user input to protect against common web vulnerabilities, including injection, cross-site scripting, and cross-site request forgery.
- **NFR-14:** The system shall record security-relevant events, including successful and failed logins, authorization failures, account changes, and administrative actions, in an audit log.
- **NFR-15:** The system shall collect only personal information necessary for event and volunteer management and shall provide authorized administrators with the ability to manage or delete personal data in accordance with applicable privacy policies.

### 2.5 Usability and Accessibility

- **NFR-16:** The system shall provide a responsive interface that remains usable on desktop computers, tablets, and mobile phones with screen widths from 320 pixels upward.
- **NFR-17:** The system shall use consistent navigation, terminology, form layouts, and feedback messages across all user roles.
- **NFR-18:** The system shall display validation messages next to invalid or missing form fields and shall explain how users can correct the input.

### 2.6 Maintainability and Supportability

- **NFR-19:** The system shall use a modular architecture that separates presentation, business logic, data access, and authentication/authorization concerns.
- **NFR-20:** The system shall maintain automated logs for application errors, performance issues, and important background processes, without recording passwords or unnecessary sensitive information.
- **NFR-21:** The system shall provide automated tests for critical workflows, including authentication, event creation, volunteer registration, application approval, capacity enforcement, and attendance recording.
- **NFR-22:** The system shall document its public APIs, database schema, deployment procedure, backup procedure, and configuration requirements.


### 2.7 Compatibility and Portability

- **NFR-23:** The system shall support the latest two stable versions of major modern browsers, including Google Chrome, Mozilla Firefox, Microsoft Edge, and Apple Safari.
- **NFR-24:** The system shall use a database and deployment configuration that can be moved to another supported hosting environment without changing business rules or losing application data.
- **NFR-25:** The system shall use a consistent time-zone strategy and shall display event dates and times in the relevant event or user time zone to prevent scheduling ambiguity.

## External Interfaces and Dependencies

- The application backend integrates with an external Email Service over SMTP/HTTPS for account registration/verification and volunteer application status messages (FR-01, FR-12). External-service wait time is excluded as specified by NFR-03.
- The application performs automated daily MySQL backups to offsite Cloud Backup Storage over HTTPS, with a minimum 30-day retention target and recovery support for the 4-hour restoration objective (NFR-06, NFR-07).