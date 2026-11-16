# Report

## Project progress

Step 4 architecture documentation describes the Event & Volunteer Management System as a three-tier React frontend, Node.js/Express backend, and MySQL database. The C4 context, container, and component diagrams retain the Volunteer, Event Organizer, and Administrator actors and now include two external systems:

- **Email Service:** backend sends account registration/verification and application status emails over SMTP/HTTPS, supporting FR-01 and FR-12. NFR-03 excludes external-service waiting from request timing.
- **Cloud Backup Storage:** backend scheduled process uploads daily MySQL backups over HTTPS. Configure 30-day retention to address NFR-06; backups and a restore procedure support NFR-07's four-hour recovery objective.

PlantUML sources are in `uml/`; the rendered images are in `uml/rendered/`. The requirements-to-architecture mappings are in `docs/traceability_matrix.md`. Existing numbered requirements FR-01–FR-21 and NFR-01–NFR-32 were not changed. These are design artifacts; implementation, provider selection/configuration, and recovery verification remain future work.