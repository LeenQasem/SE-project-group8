# Traceability Matrix

This matrix records the current logical architecture mapping. It does not claim that implementation or verification is complete.

| Requirement | Architecture element / relationship | Evidence |
|---|---|---|
| FR-01 | User Management triggers Email Notifications for account registration/verification; notification component sends via SMTP/HTTPS to Email Service. | C4 Level 3 `uml/component.puml`; `docs/architecture.md` |
| FR-12 | Application Management triggers Email Notifications after organizer approval/rejection; Email Service delivers status messages. | C4 Level 3 `uml/component.puml`; `docs/architecture.md` |
| NFR-03 | Backend API workflow; external Email Service wait is excluded from request completion timing as the requirement specifies. | `docs/requirements.md`; `docs/architecture.md` |
| NFR-06 | Scheduled Backup & Recovery exports MySQL application data daily and uploads offsite to Cloud Backup Storage; configure minimum 30-day retention. | C4 Levels 1–3; `docs/architecture.md` |
| NFR-07 | Cloud backup plus restore procedure supports recovery and restoration within the four-hour target; target requires operational runbook and tested recovery. | C4 Level 3; `docs/architecture.md` |
| FR-02–FR-11, FR-13–FR-21 | React / Express / MySQL use cases and role-based interactions remain as described in the requirements and architecture. | `docs/requirements.md`; `docs/architecture.md`; C4 diagram sources |
| NFR-01–NFR-02, NFR-04–NFR-05, NFR-08–NFR-32 | Existing functional and quality architecture constraints remain applicable; no numbered requirement was changed by this architecture update. | `docs/requirements.md` |

## External interface notes

- Email Service: outbound account registration/verification and application decision emails over SMTP/HTTPS; external waiting excluded by NFR-03.
- Cloud Backup Storage: daily offsite MySQL backups over HTTPS, at least 30 days retention, and restoration support aligned to NFR-06/NFR-07.