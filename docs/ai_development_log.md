# AI Development Log

| Version | Agent | Task / Prompt Ref. | Changed Modules | Issues / Corrections | Student Review |
|---|---|---|---|---|---|
| v0.4.0-design | Codex | Requirements and system architecture — [step4_architecture.md](../prompts/step4_architecture.md) | Requirements, architecture, C4 context/container/component views, traceability, report, README | Added external email and cloud backup systems; linked email to FR-01 / FR-12 and NFR-03, and backup/restore to NFR-06 / NFR-07. Preserved numbered requirements and recorded dependencies. | [Reviewed by Team Member] |
| v0.4.1-design | Codex | System Architecture + External Systems — [step4_architecture.md](../prompts/step4_architecture.md) | Architecture documentation, C4 diagrams, requirements dependency note, traceability, report, README | Added Email Service and Cloud Backup Storage to C4 Levels; documented daily offsite backups, 30-day retention, and recovery support without claiming implementation. | [Reviewed by Team Member] |
| v0.4.2-design | Codex | Deployment View — [step4_architecture.md](../prompts/step4_architecture.md) | Deployment diagram, architecture, traceability, report | Added vendor-neutral browser, scalable application, private database, email, and backup nodes; linked choices to relevant NFRs. | [Reviewed by Team Member] |
| v0.5.0-design | Codex | UML Class Diagram — [step5_class_diagram.md](../prompts/step5_class_diagram.md) | UML class model | Corrected the modeling note to state Attendance is associated with Volunteer and Event; documented assumptions and retained the organizer recording association in the model. | [Reviewed by Team Member] |
| v0.6.0-plan | Codex | Incremental Development Plan (no dedicated prompt record; nearest existing prompt: [step5_class_diagram.md](../prompts/step5_class_diagram.md)) | Incremental development plan | Plan outline is present in `docs/incremental_development_plan.md`; no separate prompt record for this milestone exists in `/prompts/`. | [Reviewed by Team Member] |

| v0.1.0-design | Codex | Increment 1 Class Diagram — [class_diagram_increment1_prompt.md](../prompts/class_diagram_increment1_prompt.md) | Increment 1 UML class design | Aligned the scoped class model with the ERD; omitted unsupported account-status and session-persistence details. Rendering was unavailable (PlantUML/Java/image renderer absent). | Pending team review |

