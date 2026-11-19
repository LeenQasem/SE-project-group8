# Use Case Descriptions

## 1. Purpose

These descriptions document the principal interactions shown in `uml/use_case_diagram.puml` and supported by the Functional Requirements in `docs/requirements.md`. The diagram's UC numbers are retained as use case IDs. Where the requirements do not specify behavior, the gap is identified instead of being filled by assumption.

## 2. Selected Important Use Cases

| Use Case ID | Use Case Name |
|---|---|
| UC-01 | Create a User Account |
| UC-02 | User Login and Logout |
| UC-03 | User Roles Management |
| UC-04 | Role-Based Access Control |
| UC-05 | Create Events |
| UC-06 | Edit and Cancel Events |
| UC-07 | Browse Events |
| UC-08 | Search Events |
| UC-09 | View Event Details |
| UC-10 | Apply for Events |
| UC-11 | View Event Applications |
| UC-12 | Approve or Reject Applications |
| UC-13 | View Application Status |
| UC-14 | Assign Tasks to Volunteers |
| UC-15 | View Assigned Tasks |
| UC-16 | Record Volunteer Attendance |
| UC-17 | Calculate Volunteer Hours |
| UC-18 | View Attendance Records and Total Hours |
| UC-19 | View Event Participation Statistics |
| UC-20 | Manage User Accounts |
| UC-21 | View Overall Platform Statistics |
| UC-22 | Perform Automated Daily Backup |
| UC-23 | Recover Service and Restore Data |

## 3. Detailed Use Case Descriptions

### UC-01 — Create a User Account

| Field | Description |
|---|---|
| Use Case ID | UC-01 |
| Use Case Name | Create a User Account |
| Primary Actor | User |
| Secondary Actors | Email Service |
| Description | Allows a user to register an account with a name, email address, and password. |
| Preconditions | The user is not currently registered with the supplied email address. |
| Postconditions | On success, a new account is saved and account creation is confirmed. |
| Main Success Scenario | 1. **User:** Provides a name, email address, and password. <br>2. **System:** Validates the information and checks whether the email address is already registered. <br>3. **System:** Saves the new account. <br>4. **System:** Confirms account creation. |
| Alternative Flows | None specified. |
| Exception Flows | **At step 2:** If the email is invalid or already registered, the system does not create the account. The exact response is unspecified. |
| Related Functional Requirements | FR-01 |

### UC-02 — User Login and Logout

| Field | Description |
|---|---|
| Use Case ID | UC-02 |
| Use Case Name | User Login and Logout |
| Primary Actor | User |
| Secondary Actors | None specified |
| Description | Allows a registered user to start or end an authenticated session. |
| Preconditions | For login, the user has a registered account. For logout, the user has an active session. |
| Postconditions | Successful login creates a session; successful logout ends it. |
| Main Success Scenario | 1. **User:** Provides an email address and password to log in. <br>2. **System:** Verifies the credentials. <br>3. **System:** Creates a session and confirms login. <br>4. **User:** Selects the logout action. <br>5. **System:** Ends the session and confirms logout. |
| Alternative Flows | Login and logout may occur as separate interactions; the requirements do not prescribe a combined sequence. |
| Exception Flows | **At step 2:** If credentials are invalid or the user is not registered, login is refused. The exact response is unspecified. |
| Related Functional Requirements | FR-02 |

### UC-03 — User Roles Management

| Field | Description |
|---|---|
| Use Case ID | UC-03 |
| Use Case Name | User Roles Management |
| Primary Actor | Administrator |
| Secondary Actors | None specified |
| Description | Assigns and stores one of the system's defined roles for a user account. |
| Preconditions | The account exists. The role assignment mechanism and timing are unspecified. |
| Postconditions | The account has one of the defined roles: Administrator, Event Organizer, or Volunteer. |
| Main Success Scenario | 1. **Administrator:** Supplies role information for a user account. <br>2. **System:** Checks that the role is one of the three defined roles. <br>3. **System:** Assigns and stores the role. <br>4. **System:** Confirms the role assignment. |
| Alternative Flows | None specified. |
| Exception Flows | **At step 2:** If the role is not one of the three defined roles, the assignment cannot be completed. Exact response unspecified. |
| Related Functional Requirements | FR-03 |

### UC-04 — Role-Based Access Control

| Field | Description |
|---|---|
| Use Case ID | UC-04 |
| Use Case Name | Role-Based Access Control |
| Primary Actor | User |
| Secondary Actors | None specified |
| Description | Checks whether an authenticated user's role permits access to a requested protected feature. The diagram states that this applies to every protected operation and shows representative include links. |
| Preconditions | The user is authenticated, has an assigned role, and requests a protected feature. |
| Postconditions | Access is granted or denied according to the user's role. |
| Main Success Scenario | 1. **User:** Requests a protected feature. <br>2. **System:** Checks the user's role against permissions for the feature. <br>3. **System:** Grants access if the role is permitted. |
| Alternative Flows | **At step 3:** If the role is not permitted, the system denies access. |
| Exception Flows | Behavior when authentication or role information is unavailable is unspecified. |
| Related Functional Requirements | FR-04 |

### UC-05 — Create Events

| Field | Description |
|---|---|
| Use Case ID | UC-05 |
| Use Case Name | Create Events |
| Primary Actor | Event Organizer |
| Secondary Actors | None specified |
| Description | Allows an Event Organizer to create an event with its title, description, date, location, and required volunteer capacity. |
| Preconditions | The actor is authenticated and has the Event Organizer role. |
| Postconditions | An event record is saved and creation is confirmed. |
| Main Success Scenario | 1. **Event Organizer:** Provides the event title, description, date, location, and required capacity. <br>2. **System:** Validates the information, including that capacity is a positive whole number. <br>3. **System:** Saves the new event. <br>4. **System:** Confirms creation. |
| Alternative Flows | None specified. |
| Exception Flows | **At step 2:** If information is invalid or capacity is not a positive whole number, the system does not create the event. Exact response unspecified. |
| Related Functional Requirements | FR-05; FR-04 applies as a protected operation. |

### UC-06 — Edit and Cancel Events

| Field | Description |
|---|---|
| Use Case ID | UC-06 |
| Use Case Name | Edit and Cancel Events |
| Primary Actor | Event Organizer |
| Secondary Actors | None specified |
| Description | Allows an Event Organizer to edit or cancel an event they own. |
| Preconditions | The actor is authenticated, has the Event Organizer role, and the selected event exists. |
| Postconditions | On edit, event details are updated. On cancellation, the event is cancelled and cannot accept new applications. |
| Main Success Scenario | 1. **Event Organizer:** Selects an event and requests an edit or cancellation. <br>2. **System:** Verifies that the event belongs to the organizer. <br>3. **System:** Applies the requested edit or cancellation. <br>4. **System:** Confirms the change. |
| Alternative Flows | **At step 1:** The organizer edits event information or requests cancellation. |
| Exception Flows | **At step 2:** If the event is not owned by the organizer, the requested change is not permitted. Exact response unspecified. |
| Related Functional Requirements | FR-06; FR-04 applies as a protected operation. |

### UC-07 — Browse Events

| Field | Description |
|---|---|
| Use Case ID | UC-07 |
| Use Case Name | Browse Events |
| Primary Actor | Volunteer |
| Secondary Actors | None specified |
| Description | Displays events that are open for applications and have remaining volunteer capacity. |
| Preconditions | The actor is a Volunteer. Authentication requirements for browsing are unspecified. |
| Postconditions | A list of available events is displayed. |
| Main Success Scenario | 1. **Volunteer:** Requests to browse events, optionally providing criteria. <br>2. **System:** Retrieves events open for applications with available capacity. <br>3. **System:** Displays the available events. |
| Alternative Flows | **At step 1:** The volunteer may supply optional browsing criteria. |
| Exception Flows | Behavior if no events match or event data cannot be retrieved is unspecified. |
| Related Functional Requirements | FR-07 |

### UC-08 — Search Events

| Field | Description |
|---|---|
| Use Case ID | UC-08 |
| Use Case Name | Search Events |
| Primary Actor | Volunteer |
| Secondary Actors | None specified |
| Description | Searches events using text and optional date or location filters. The diagram models this use case as an extension of Browse Events. |
| Preconditions | The actor is a Volunteer. Authentication requirements for searching are unspecified. |
| Postconditions | Matching events are displayed, excluding cancelled and fully staffed events. |
| Main Success Scenario | 1. **Volunteer:** Enters search text and optionally date or location filters. <br>2. **System:** Searches event titles, descriptions, dates, and locations using the criteria. <br>3. **System:** Excludes cancelled and fully staffed events. <br>4. **System:** Displays matching events. |
| Alternative Flows | **At step 1:** Date and location filters may be omitted. |
| Exception Flows | Behavior if no events match is unspecified. |
| Related Functional Requirements | FR-08; extends FR-07. |

### UC-09 — View Event Details

| Field | Description |
|---|---|
| Use Case ID | UC-09 |
| Use Case Name | View Event Details |
| Primary Actor | Volunteer |
| Secondary Actors | None specified |
| Description | Displays details for a selected event. The diagram models this use case as an extension of Browse Events. |
| Preconditions | The actor is a Volunteer and has an event ID. Authentication requirements are unspecified. |
| Postconditions | The event title, description, date, location, required capacity, and status are displayed. |
| Main Success Scenario | 1. **Volunteer:** Selects an event by ID. <br>2. **System:** Retrieves the event. <br>3. **System:** Displays its details. |
| Alternative Flows | None specified. |
| Exception Flows | **At step 2:** If the event ID is invalid, details are not returned. Exact response unspecified. |
| Related Functional Requirements | FR-09; extends FR-07. |

### UC-10 — Apply for Events

| Field | Description |
|---|---|
| Use Case ID | UC-10 |
| Use Case Name | Apply for Events |
| Primary Actor | Volunteer |
| Secondary Actors | None specified |
| Description | Allows a Volunteer to apply for an event that is not cancelled or full, provided they have not already applied. |
| Preconditions | The actor is authenticated and has the Volunteer role. The event exists and is open to applications. |
| Postconditions | An application is saved with Pending status and confirmation is provided. |
| Main Success Scenario | 1. **Volunteer:** Selects an event and submits an application. <br>2. **System:** Checks that the event is not cancelled or full and that the volunteer has not already applied. <br>3. **System:** Saves the application with Pending status. <br>4. **System:** Confirms the application. |
| Alternative Flows | None specified. |
| Exception Flows | **At step 2:** If the event is cancelled or full, or the volunteer already applied, the application is not saved. Exact response unspecified. |
| Related Functional Requirements | FR-10; FR-04 applies as a protected operation. |

### UC-11 — View Event Applications

| Field | Description |
|---|---|
| Use Case ID | UC-11 |
| Use Case Name | View Event Applications |
| Primary Actor | Event Organizer |
| Secondary Actors | None specified |
| Description | Displays applications and their statuses for an event owned by the Event Organizer. |
| Preconditions | The actor is authenticated, has the Event Organizer role, and the event exists. |
| Postconditions | Applications and statuses for the organizer's event are displayed. |
| Main Success Scenario | 1. **Event Organizer:** Selects an event. <br>2. **System:** Verifies event ownership. <br>3. **System:** Retrieves applications and statuses for the event. <br>4. **System:** Displays the applications. |
| Alternative Flows | None specified. |
| Exception Flows | **At step 2:** If the event does not belong to the organizer, access is denied. Exact response unspecified. |
| Related Functional Requirements | FR-11; FR-04 applies as a protected operation. |

### UC-12 — Approve or Reject Applications

| Field | Description |
|---|---|
| Use Case ID | UC-12 |
| Use Case Name | Approve or Reject Applications |
| Primary Actor | Event Organizer |
| Secondary Actors | Email Service |
| Description | Allows an Event Organizer to decide an application for an event they own, subject to application status and event capacity. |
| Preconditions | The actor is authenticated, has the Event Organizer role, and the application belongs to an event they own. |
| Postconditions | The application status is updated to Approved or Rejected. |
| Main Success Scenario | 1. **Event Organizer:** Selects an application and submits an approval or rejection decision. <br>2. **System:** Verifies event ownership and checks application status and available capacity. <br>3. **System:** Updates the status according to the decision, ensuring approved volunteers do not exceed capacity. <br>4. **System:** Confirms the updated status. |
| Alternative Flows | **At step 1:** The organizer approves or rejects the application. |
| Exception Flows | **At step 2:** If the event is not owned by the organizer, the status does not change. If capacity is insufficient, approval cannot be completed. Behavior for other invalid statuses is unspecified. |
| Related Functional Requirements | FR-12; FR-04 applies as a protected operation. |

**Email Service clarification:** The diagram and external interfaces text associate the Email Service with application decisions and status messages. FR-12 does not specify whether a message must be sent, its content, or behavior if the service is unavailable.

### UC-13 — View Application Status

| Field | Description |
|---|---|
| Use Case ID | UC-13 |
| Use Case Name | View Application Status |
| Primary Actor | Volunteer |
| Secondary Actors | None specified |
| Description | Displays the current statuses of applications submitted by the Volunteer. |
| Preconditions | The actor is authenticated and has the Volunteer role. |
| Postconditions | The volunteer's applications and Pending, Approved, or Rejected statuses are displayed. |
| Main Success Scenario | 1. **Volunteer:** Requests application status. <br>2. **System:** Retrieves applications submitted by that volunteer and their statuses. <br>3. **System:** Displays the applications and statuses. |
| Alternative Flows | None specified. |
| Exception Flows | Behavior if the volunteer has no applications or the data is unavailable is unspecified. |
| Related Functional Requirements | FR-13; FR-04 applies as a protected operation. |

### UC-14 — Assign Tasks to Volunteers

| Field | Description |
|---|---|
| Use Case ID | UC-14 |
| Use Case Name | Assign Tasks to Volunteers |
| Primary Actor | Event Organizer |
| Secondary Actors | None specified |
| Description | Allows an Event Organizer to assign a task to a volunteer approved for the relevant event. |
| Preconditions | The actor is authenticated, has the Event Organizer role, and the volunteer is approved for the event. |
| Postconditions | The task assignment is saved and confirmation and task details are provided. |
| Main Success Scenario | 1. **Event Organizer:** Provides event ID, volunteer ID, task name, and description. <br>2. **System:** Verifies the volunteer is approved for the event. <br>3. **System:** Saves the task assignment. <br>4. **System:** Confirms the assignment and its details. |
| Alternative Flows | None specified. |
| Exception Flows | **At step 2:** If the volunteer is not approved for the event, the task is not assigned. Exact response unspecified. |
| Related Functional Requirements | FR-14; FR-04 applies as a protected operation. |

### UC-15 — View Assigned Tasks

| Field | Description |
|---|---|
| Use Case ID | UC-15 |
| Use Case Name | View Assigned Tasks |
| Primary Actor | Volunteer |
| Secondary Actors | None specified |
| Description | Displays tasks assigned to the Volunteer. |
| Preconditions | The actor is authenticated and has the Volunteer role. |
| Postconditions | The volunteer's assigned tasks and details are displayed. |
| Main Success Scenario | 1. **Volunteer:** Requests assigned tasks. <br>2. **System:** Retrieves tasks assigned to that volunteer. <br>3. **System:** Displays the tasks and details. |
| Alternative Flows | None specified. |
| Exception Flows | Behavior if the volunteer has no assigned tasks or the data is unavailable is unspecified. |
| Related Functional Requirements | FR-15; FR-04 applies as a protected operation. |

### UC-16 — Record Volunteer Attendance

| Field | Description |
|---|---|
| Use Case ID | UC-16 |
| Use Case Name | Record Volunteer Attendance |
| Primary Actor | Event Organizer |
| Secondary Actors | None specified |
| Description | Allows an authorized Event Organizer to manually record a volunteer's attendance for their event. |
| Preconditions | The actor is authenticated and authorized for the event. Event and volunteer information is valid. |
| Postconditions | The attendance record is saved and confirmation is provided. |
| Main Success Scenario | 1. **Event Organizer:** Provides event ID, volunteer ID, and attendance status. <br>2. **System:** Verifies the event and volunteer information and the organizer's authority. <br>3. **System:** Saves the attendance record. <br>4. **System:** Confirms the record was saved. |
| Alternative Flows | None specified. |
| Exception Flows | **At step 2:** If information is invalid or the organizer is not authorized for the event, the record is not saved. Exact response unspecified. |
| Related Functional Requirements | FR-16; FR-04 applies as a protected operation. |

### UC-17 — Calculate Volunteer Hours

| Field | Description |
|---|---|
| Use Case ID | UC-17 |
| Use Case Name | Calculate Volunteer Hours |
| Primary Actor | Event Organizer |
| Secondary Actors | None specified |
| Description | Stores hours entered by the organizer and calculates a volunteer's total across events. The diagram shows this use case included by Record Volunteer Attendance. |
| Preconditions | Attendance information exists and the organizer has entered hours for the relevant participation. |
| Postconditions | Valid recorded hours are included in the volunteer's updated total. |
| Main Success Scenario | 1. **Event Organizer:** Enters volunteer hours associated with attendance records. <br>2. **System:** Checks that entered hours are non-negative. <br>3. **System:** Stores entered hours and calculates the volunteer's total across events using valid recorded hours. <br>4. **System:** Makes the updated total available. |
| Alternative Flows | The diagram links this use case to attendance recording with `<<include>>`; whether hours are entered at attendance-recording time is unspecified. |
| Exception Flows | **At step 2:** Negative hours are invalid and are not included. Exact response unspecified. |
| Related Functional Requirements | FR-17; included by FR-16 in the diagram. |

### UC-18 — View Attendance Records and Total Hours

| Field | Description |
|---|---|
| Use Case ID | UC-18 |
| Use Case Name | View Attendance Records and Total Hours |
| Primary Actor | Volunteer |
| Secondary Actors | None specified |
| Description | Displays the Volunteer's attendance history and total recorded volunteer hours. |
| Preconditions | The actor is authenticated and has the Volunteer role. |
| Postconditions | The volunteer's attendance records and total hours are displayed. |
| Main Success Scenario | 1. **Volunteer:** Requests attendance records and total hours. <br>2. **System:** Retrieves that volunteer's records and total recorded hours. <br>3. **System:** Displays the records and total. |
| Alternative Flows | None specified. |
| Exception Flows | Behavior if the volunteer has no records or the data is unavailable is unspecified. |
| Related Functional Requirements | FR-18; FR-04 applies as a protected operation. |

### UC-19 — View Event Participation Statistics

| Field | Description |
|---|---|
| Use Case ID | UC-19 |
| Use Case Name | View Event Participation Statistics |
| Primary Actor | Event Organizer |
| Secondary Actors | None specified |
| Description | Displays participation statistics for an event owned by the Event Organizer. |
| Preconditions | The actor is authenticated, has the Event Organizer role, and the event exists. |
| Postconditions | Application counts, attendance counts, and volunteer hours for the event are displayed. |
| Main Success Scenario | 1. **Event Organizer:** Selects an event for statistics. <br>2. **System:** Verifies event ownership. <br>3. **System:** Calculates statistics using application and attendance records. <br>4. **System:** Displays the statistics. |
| Alternative Flows | None specified. |
| Exception Flows | **At step 2:** If the event is not owned by the organizer, its statistics are not made available. Exact response unspecified. |
| Related Functional Requirements | FR-19; FR-04 applies as a protected operation. |

### UC-20 — Manage User Accounts

| Field | Description |
|---|---|
| Use Case ID | UC-20 |
| Use Case Name | Manage User Accounts |
| Primary Actor | Administrator |
| Secondary Actors | None specified |
| Description | Allows an Administrator to update a selected user account or perform an account management action. |
| Preconditions | The actor is authenticated and has the Administrator role. The selected account exists. |
| Postconditions | The account is updated and confirmation is provided. |
| Main Success Scenario | 1. **Administrator:** Selects a user by ID and supplies account information or a management action. <br>2. **System:** Verifies administrator authorization. <br>3. **System:** Updates the selected account. <br>4. **System:** Confirms the update. |
| Alternative Flows | The requirements permit account information changes or a management action but do not define the specific actions. |
| Exception Flows | **At step 2:** If the actor is not authorized, account management is denied. Exact response unspecified. |
| Related Functional Requirements | FR-20; FR-04 applies as a protected operation. |

### UC-21 — View Overall Platform Statistics

| Field | Description |
|---|---|
| Use Case ID | UC-21 |
| Use Case Name | View Overall Platform Statistics |
| Primary Actor | Administrator |
| Secondary Actors | None specified |
| Description | Displays platform-wide summaries derived from user, event, application, and volunteer-hours data. |
| Preconditions | The actor is authenticated and has the Administrator role. |
| Postconditions | Overall platform statistics and summaries are displayed. |
| Main Success Scenario | 1. **Administrator:** Requests platform statistics and may provide date filters. <br>2. **System:** Aggregates user, event, application, and volunteer-hours data. <br>3. **System:** Displays statistics and summaries. |
| Alternative Flows | **At step 1:** Date filters may be provided or omitted. |
| Exception Flows | Behavior if platform data is unavailable or a filter is invalid is unspecified. |
| Related Functional Requirements | FR-21; FR-04 applies as a protected operation. |

### UC-22 — Perform Automated Daily Backup

| Field | Description |
|---|---|
| Use Case ID | UC-22 |
| Use Case Name | Perform Automated Daily Backup |
| Primary Actor | Not specified; the diagram shows no initiating human actor. |
| Secondary Actors | Cloud Backup Storage |
| Description | Represents the diagrammed daily backup of application data to offsite storage. |
| Preconditions | Application data is available for backup and Cloud Backup Storage can be reached. The initiating mechanism is unspecified. |
| Postconditions | On success, a backup is stored offsite. The stated retention target is at least 30 days. |
| Main Success Scenario | 1. **System:** Initiates the automated daily backup. <br>2. **System:** Transfers the backup to Cloud Backup Storage over HTTPS, as stated in the external interfaces section. <br>3. **Cloud Backup Storage:** Stores the backup. |
| Alternative Flows | None specified. |
| Exception Flows | Retry, alerting, or recovery behavior if backup or storage fails is unspecified. |
| Related Functional Requirements | None. Related non-functional requirement: NFR-02. The external interfaces section also cites NFR-06 and NFR-07 for backup behavior, but these IDs refer to scalability and capacity requirements in the SRS. |

### UC-23 — Recover Service and Restore Data

| Field | Description |
|---|---|
| Use Case ID | UC-23 |
| Use Case Name | Recover Service and Restore Data |
| Primary Actor | Not specified; the diagram shows no initiating human actor. |
| Secondary Actors | Cloud Backup Storage |
| Description | Represents service recovery and data restoration after a failure. |
| Preconditions | A service failure has occurred and a usable backup is available. Who declares an incident or initiates recovery is unspecified. |
| Postconditions | Service is restored to normal operation within the stated four-hour objective after a declared incident. |
| Main Success Scenario | 1. **Unspecified operations role/system:** Initiates recovery after an incident is declared. <br>2. **System:** Retrieves backup data from Cloud Backup Storage. <br>3. **System:** Restores data and service. <br>4. **System:** Resumes normal operation within the recovery objective. |
| Alternative Flows | None specified. |
| Exception Flows | Behavior if a backup is unavailable or restoration fails is unspecified. |
| Related Functional Requirements | None. Related non-functional requirement: NFR-03. |

## 4. Traceability Table

| Use Case ID | Use Case Name | Related Functional Requirement IDs |
|---|---|---|
| UC-01 | Create a User Account | FR-01 |
| UC-02 | User Login and Logout | FR-02 |
| UC-03 | User Roles Management | FR-03 |
| UC-04 | Role-Based Access Control | FR-04 |
| UC-05 | Create Events | FR-05; FR-04 applies |
| UC-06 | Edit and Cancel Events | FR-06; FR-04 applies |
| UC-07 | Browse Events | FR-07 |
| UC-08 | Search Events | FR-08; extends FR-07 |
| UC-09 | View Event Details | FR-09; extends FR-07 |
| UC-10 | Apply for Events | FR-10; FR-04 applies |
| UC-11 | View Event Applications | FR-11; FR-04 applies |
| UC-12 | Approve or Reject Applications | FR-12; FR-04 applies |
| UC-13 | View Application Status | FR-13; FR-04 applies |
| UC-14 | Assign Tasks to Volunteers | FR-14; FR-04 applies |
| UC-15 | View Assigned Tasks | FR-15; FR-04 applies |
| UC-16 | Record Volunteer Attendance | FR-16; FR-04 applies |
| UC-17 | Calculate Volunteer Hours | FR-17; included by FR-16 in the diagram |
| UC-18 | View Attendance Records and Total Hours | FR-18; FR-04 applies |
| UC-19 | View Event Participation Statistics | FR-19; FR-04 applies |
| UC-20 | Manage User Accounts | FR-20; FR-04 applies |
| UC-21 | View Overall Platform Statistics | FR-21; FR-04 applies |
| UC-22 | Perform Automated Daily Backup | None specified; related NFR-02 |
| UC-23 | Recover Service and Restore Data | None specified; related NFR-03 |

## 5. Validation Findings and Missing Information

- All 23 use cases documented above appear in `uml/use_case_diagram.puml`.
- FR-01 through FR-21 referenced here exist in `docs/requirements.md`. UC-22 and UC-23 have no corresponding functional requirement; their related behavior is expressed as non-functional requirements.
- Human actors match the diagram: User, Administrator, Event Organizer, and Volunteer. Email Service is associated with UC-01 and UC-12; Cloud Backup Storage with UC-22 and UC-23. The diagram does not identify a human initiator for backup or recovery.
- FR-04 is stated to apply to every protected operation, while only representative include links are drawn. This document notes FR-04 for protected operations without adding diagram relationships.
- Registration verification and application-decision email behavior are mentioned by the diagram/external interfaces but are not fully specified by FR-01 or FR-12. Verification rules, message conditions/content, and external-service failure behavior require clarification.
- The external interfaces section cites NFR-06 and NFR-07 for backup/retention, but those numbers identify scalability and capacity requirements in the SRS. NFR-02 describes backups and NFR-03 describes recovery.
- Several validation and ownership constraints do not define exact error messages, retry behavior, or empty-result behavior. These descriptions identify those gaps without prescribing unsupported responses.
