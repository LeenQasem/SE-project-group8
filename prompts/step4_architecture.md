# Step 4 — System Architecture: Prompt Record

## User request

Complete Step 4 for the Event & Volunteer Management System (React frontend, Node.js/Express backend, MySQL database): document the three-tier client-server architecture and C4 Level 1 (System Context), Level 2 (Container), and Level 3 (Component); link the documentation to PNG diagrams under `uml/rendered/`; create PlantUML sources and render PNGs; create this prompt record and a Step 4 entry in the AI development log. Do not write application code.

## Architecture inputs used

- `README.md`: system purpose, three roles, technology summary, and intended event/volunteer workflows.
- `docs/requirements.md`: FR-01–FR-21 covering accounts and roles, event management, applications, task assignment, attendance/hours, and reports/administration.
- User-provided stack clarification: React frontend, Node.js/Express backend, MySQL database.

## Decisions recorded

- Use a logical three-tier client-server model: React presentation tier, Express application tier, and MySQL data tier. The browser communicates with the backend over HTTPS/JSON; only the backend accesses MySQL.
- Treat the three C4 views at their requested levels. Level 1 shows the three human actors and the system; Level 2 shows frontend/backend/database containers; Level 3 expands backend responsibilities into API, access-control, domain-service, and data-access components.
- Component boundaries are a proposed logical design derived from requirements; no application modules or code are represented as already implemented.
- Keep hosting topology, API contracts, authentication mechanism, and detailed schema unspecified because project materials do not define them.
- Save editable diagrams as PlantUML in `uml/` and export PNG views to `uml/rendered/`.

## Scope boundary

This step changes architecture documentation, the AI log, the prompt record, and diagram artifacts only. No application code is part of this work.