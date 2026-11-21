# Step 6 Prompt: Project Description

## Task
Write a complete, formal project description for the CS13477 project, Event & Volunteer Management System, in `docs/project_description.md`.

## Source files to inspect
- `docs/requirements.md`
- `docs/architecture.md`
- `docs/incremental_development_plan.md`
- `uml/system_context.puml`
- `uml/container.puml`
- `uml/component.puml`
- `uml/deployment.puml`
- `uml/class_diagram.puml`
- `uml/sequence_diagram.mmd`

## Required sections
1. **Project Overview & Purpose** — Describe the web platform for organizing community and institutional events and coordinating volunteers. Explain how it addresses manual tracking, scattered applications, attendance verification, and capacity management.
2. **Target Users & Roles** — Describe Volunteer, Event Organizer, and Administrator based on the system context, requirements, and class diagram.
3. **Core System Capabilities (Scope)** — Cover authentication and role-based access; events and capacity; application and approval workflow with email notifications; task assignment; attendance and hours; statistics and reporting. Use modeled entities and enums where relevant: `User`, `UserRole`, `Event`, `EventStatus`, `Application`, `ApplicationStatus`, `Task`, `TaskStatus`, `Attendance`, `Report`, and `ReportType`.
4. **Technical Architecture & Technology Stack** — Explain the three-tier React SPA, Python backend and its component responsibilities, MySQL relational database, HTTPS/TLS and at-rest protection, Email Service over SMTP/HTTPS, and automated daily offsite Cloud Backup Storage with at least 30-day retention and a four-hour recovery objective. Do not select a Python web framework unless approved separately.
5. **Development Methodology & Project Goals** — State that development is incremental, uses Agentic AI workflows, maintains requirements-to-code-to-test traceability, and follows the version progression `v0.x.0-design` -> `v0.x.0` -> `v1.0.0`.

## Consistency and writing constraints
- Use clear formal academic/technical English suitable for a university Software Engineering submission.
- Preserve the exact role, entity, enum, component, and technology names in the supplied sources.
- Do not claim implementation, testing, provider selection, or deployment configuration is complete unless a source explicitly establishes it.
- Treat architecture and UML as design descriptions; distinguish planned capabilities from completed implementation.
- Refer to requirement IDs only when useful and preserve their source meaning. Requirements include email notification for registration/verification and application decisions; daily backup retention of at least 30 days; and restoration within four hours.
- Write the complete Markdown document directly to `docs/project_description.md`, replacing its placeholder.
