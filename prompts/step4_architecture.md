# Step 4 System Architecture: Prompt Record

## User request

Complete Step 4 for the Event & Volunteer Management System using React, Node.js/Express, and MySQL. Document the three-tier client-server architecture and C4 Levels , create PlantUML sources and rendered PNGs, and log the work without writing application code. The architecture includes these requirement-linked external systems:

- **Email Service (`System_Ext`):** application backend sends account registration/verification and volunteer application status emails over SMTP/HTTPS; supports FR-01, FR-12, with external wait excluded by NFR-03.
- **Cloud Backup Storage (`System_Ext`):** backend scheduled process uploads automated daily MySQL backups over HTTPS, with 30-day retention and support for the NFR-07 four-hour recovery objective; supports NFR-06 and NFR-07.

## Architecture inputs

- `docs/requirements.md` is the source of truth for FR-01â€“FR-21 and NFR-01â€“NFR-32. Relevant requirements: FR-01, FR-12, NFR-03, NFR-06, and NFR-07.
- `docs/architecture.md`: existing React / Node.js-Express / MySQL three-tier design and role workflows.

## Decisions

- Retain Volunteer, Event Organizer, and Administrator as the human actors and preserve the three logical tiers.
- Show both external systems at C4 Levels 1 and 2. At Level 3, add Email Notifications and Scheduled Backup & Recovery backend components to show the same interactions.
- Backend initiates email delivery via SMTP/HTTPS and daily database backup uploads via HTTPS. Storage retention and recovery objectives are explicitly tied to NFR-06 and NFR-07. Do not imply integrations are implemented or provider chosen.
- Preserve existing FR/NFR statements; add only a short external interfaces/dependencies note to requirements.
- Keep exact existing rendered image names, including `system_contex.png`.

## Scope

Update architecture-related diagrams, PNGs, requirement dependency note, traceability, report, README architecture summary, this prompt record, and AI development log. No application code is written.
## Section 5.1 — Deployment View addition

Add a vendor-neutral C4 Deployment View using `C4_Deployment.puml` at `uml/deployment.puml`, render it to `uml/rendered/deployment.png`, and update architecture, traceability, report, this prompt record, and AI development log as needed. Show:

- Client Browser Node running the React frontend over HTTPS (NFR-15, NFR-21, NFR-30).
- Horizontally scalable Application Server Node serving the React bundle and running Node.js/Express (NFR-10, NFR-12, NFR-15, NFR-31).
- Private Database Server Node running MySQL with encrypted storage and backend-only SQL access (NFR-15, NFR-16, NFR-31).
- External Email Service over SMTP/TLS or HTTPS for FR-01 and FR-12 (NFR-03), and Cloud Backup Storage over HTTPS for daily backups, 30-day retention, and four-hour recovery support (NFR-06, NFR-07).

Keep the design logical and vendor-neutral; do not add unrequested features or imply implementation is complete.