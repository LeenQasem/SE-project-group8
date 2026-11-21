# Step 4 System Architecture: Prompt Record

## Section 3.3 Metadata

- **Version / Increment:** v0.1.0-design
- **Agent Name:** Codex
- **Goal:** Document the system architecture, external systems, and vendor-neutral deployment view for the Event & Volunteer Management System.
- **Relevant Requirements & UML/Architecture References:** FR-01, FR-12; NFR-03, NFR-06, NFR-07, NFR-10, NFR-12, NFR-15, NFR-16, NFR-21, NFR-30, NFR-31; `docs/requirements.md`; `docs/architecture.md`; `uml/system_context.puml`, `uml/container.puml`, `uml/component.puml`, `uml/deployment.puml`.
- **Key Instructions Sent to Agent:** Retain the React / Python / MySQL three-tier design and human roles; show email and cloud backup systems with requirements-linked interactions; add the vendor-neutral C4 Deployment View; preserve numbered requirements, avoid claiming implementation or selecting providers, and do not write application code.
- **Intended Outputs:** Updated architecture and related project documentation, editable PlantUML diagrams and rendered images, and this prompt record.
- **Acceptance Criteria:** Architecture and deployment views match stated requirements; references and traceability are updated; diagrams remain editable; no application code is written.
- **Links to Results:** `docs/architecture.md`; `docs/requirements.md`; `docs/traceability_matrix.md`; `docs/report.md`; `README.md`; `uml/system_context.puml`; `uml/container.puml`; `uml/component.puml`; `uml/deployment.puml`; `uml/rendered/system_contex.png`; `uml/rendered/container.png`; `uml/rendered/component.png`; `uml/rendered/deployment.png`; `docs/ai_development_log.md`.

## User request

Complete Step 4 for the Event & Volunteer Management System using React, Python, and MySQL. Document the three-tier client-server architecture and C4 Levels, create PlantUML sources and rendered PNGs, and log the work without writing application code. The architecture includes these requirement-linked external systems:

- **Email Service (`System_Ext`):** The application backend sends account registration/verification and volunteer application status emails over SMTP/HTTPS; supports FR-01 and FR-12, with external wait excluded by NFR-03.
- **Cloud Backup Storage (`System_Ext`):** A backend scheduled process uploads automated daily MySQL backups over HTTPS, with 30-day retention and support for the NFR-07 four-hour recovery objective; supports NFR-06 and NFR-07.

## Architecture inputs

- `docs/requirements.md` is the source of truth for FR-01–FR-21 and NFR-01–NFR-32. Relevant requirements: FR-01, FR-12, NFR-03, NFR-06, and NFR-07.
- `docs/architecture.md`: existing React / Python / MySQL three-tier design and role workflows.

## Decisions

- Retain Volunteer, Event Organizer, and Administrator as the human actors and preserve the three logical tiers.
- Show both external systems at C4 Levels 1 and 2. At Level 3, add Email Notifications and Scheduled Backup & Recovery backend components to show the same interactions.
- Backend initiates email delivery via SMTP/HTTPS and daily database backup uploads via HTTPS. Storage retention and recovery objectives are explicitly tied to NFR-06 and NFR-07. Do not imply integrations are implemented or a provider is chosen.
- Preserve existing FR/NFR statements; add only a short external interfaces/dependencies note to requirements.
- Keep exact existing rendered image names, including `system_contex.png`.

## Section 5.1 — Deployment View addition

Add a vendor-neutral C4 Deployment View using `C4_Deployment.puml` at `uml/deployment.puml`, render it to `uml/rendered/deployment.png`, and update architecture, traceability, report, this prompt record, and AI development log as needed. Show:

- Client Browser Node running the React frontend over HTTPS (NFR-15, NFR-21, NFR-30).
- Horizontally scalable Application Server Node serving the React bundle and running the Python backend (NFR-10, NFR-12, NFR-15, NFR-31).
- Private Database Server Node running MySQL with encrypted storage and backend-only SQL access (NFR-15, NFR-16, NFR-31).
- External Email Service over SMTP/TLS or HTTPS for FR-01 and FR-12 (NFR-03), and Cloud Backup Storage over HTTPS for daily backups, 30-day retention, and four-hour recovery support (NFR-06, NFR-07).

Keep the design logical and vendor-neutral; do not add unrequested features or imply implementation is complete.

