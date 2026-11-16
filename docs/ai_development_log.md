# AI Development Log

Record iterative progress, decisions, and AI-assisted development notes here.

## Step 4 Ã¢â‚¬â€ System Architecture

- Documented the React / Node.js-Express / MySQL three-tier client-server architecture and C4 Levels in `docs/architecture.md`.
- Added editable PlantUML diagram sources under `uml/` and rendered diagram artifacts under `uml/rendered/`.
- Recorded the request, source inputs, and architecture decisions in `prompts/step4_architecture.md`.
- Kept the work limited to documentation and diagrams; no application code was written.
## Step 4 architecture integration update

- Added Email Service and Cloud Backup Storage to C4 Levels, architecture documentation, and rendered diagrams.
- Mapped email workflows to FR-01 / FR-12 and NFR-03; mapped daily offsite backup, retention, and restore support to NFR-06 / NFR-07 without changing numbered requirements.
- Updated the requirements dependency note, prompt record, traceability matrix, report, and README summary. No application code was written.
## Section 5.1 — Deployment View

- Added a vendor-neutral C4 Deployment View showing browser, horizontally scalable application, private database, and external email/backup infrastructure nodes.
- Linked node and connection choices to NFR-06, NFR-07, NFR-10, NFR-12, NFR-15, NFR-16, NFR-21, NFR-30, and NFR-31; updated architecture, traceability, report, and Step 4 prompt references.
- Kept provider selection and implementation out of scope.