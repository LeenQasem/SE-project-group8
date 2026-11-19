# Use Case Diagram Prompt Record

## Objective

Create a professional, requirements-based UML use case diagram for the Event & Volunteer Management System using PlantUML.

## Project review and source of truth

- Examine the overall project before creating the diagram.
- Read `docs/incremental_development_plan.md` first.
- Use `docs/requirements.md`, `docs/project_description.md`, `README.md`, and the existing UML files for project context.
- Follow the requirements strictly and do not add functionality or actors outside the documented scope.
- Create the editable source at `uml/use_case_diagram.puml`.
- Render the diagram to `uml/rendered/use_case_diagram.png`.

## Actors

The diagram must include all system actors identified in the requirements:

- User as the generalized actor.
- Administrator.
- Event Organizer.
- Volunteer.
- Email Service.
- Cloud Backup Storage.

Administrator, Event Organizer, and Volunteer generalize from User. Email Service and Cloud Backup Storage are external actors from the documented external interfaces and dependencies.

## Required functional use cases

Represent FR-01 through FR-21:

- Create a User Account
- User Login and Logout
- User Roles Management
- Role-Based Access Control
- Create Events
- Edit and Cancel Events
- Browse Events
- Search Events
- View Event Details
- Apply for Events
- View Event Applications
- Approve or Reject Applications
- View Application Status
- Assign Tasks to Volunteers
- View Assigned Tasks
- Record Volunteer Attendance
- Calculate Volunteer Hours
- View Attendance Records and Total Hours
- View Event Participation Statistics
- Manage User Accounts
- View Overall Platform Statistics

Also include the explicitly documented operational behaviors for automated daily backup and service recovery/restoration associated with Cloud Backup Storage.

## UML notation requirements

- Use a clear system boundary.
- Use standard actor-to-use-case association links.
- Use `<<include>>` for required reused behavior.
- Use `<<extend>>` for optional or extending behavior such as event search/details where appropriate.
- Use actor generalization for Administrator, Event Organizer, and Volunteer from User.
- Preserve UML meaning; do not add unrelated relationships.
- Add a concise legend explaining association, `<<include>>`, `<<extend>>`, and generalization if it improves readability.

## Layout and arrow requirements

- Place actors at the top and use cases below them.
- Organize each actor’s use cases in a dedicated, visually separated lane or group.
- Map every connector clearly to its intended use case.
- Ensure each individual arrow or association is traceable without ambiguity.
- Do not allow connectors to intersect, overlap heavily, or form confusing clusters.
- Use horizontal, vertical, or orthogonal routing with sufficient spacing.
- Separate Volunteer and Event Organizer application actions.
- Keep Email Service links separate from human actor links.
- Keep arrows readable even in the rendered PNG, not only in the source file.

## Preview, compatibility, and validation requirements

- Use PlantUML syntax compatible with the available preview renderer.
- Avoid unsupported or version-sensitive directives.
- Check for exactly one `@startuml` and `@enduml`.
- Check that all blocks and braces are balanced.
- Run `git diff --check` after editing.
- Render and verify `uml/rendered/use_case_diagram.png`.

## Important user instructions from this chat

1. Create a professional use case diagram after examining the project and identifying every actor.
2. Follow the requirements strictly and do not add anything outside them.
3. Use association links, `<<include>>`, `<<extend>>`, and generalization.
4. Make the diagram horizontal or otherwise arrange it so the arrows are understandable.
5. Fix preview errors and version-related errors by checking the PlantUML syntax carefully.
6. Separate clustered arrows in Volunteer Applications, especially links involving Administrator, Email Service, Event Organizer, and Volunteer.
7. Put actors at the top and use cases below the actors.
8. Keep each arrow by itself and prevent arrows from intersecting or confusing the viewer.
9. Create a PNG of the final UML use case diagram in the `uml/rendered` directory.
