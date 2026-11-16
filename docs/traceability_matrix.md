# Traceability Matrix

This matrix records the current logical architecture mapping. It does not claim implementation or verification is complete.

| Requirement | Architecture element / relationship | Evidence |
|---|---|---|
| FR-01 | User Management triggers registration/verification emails through Email Notifications and Email Service. | C4 Level 3 `uml/component.puml`; Deployment View `uml/deployment.puml` |
| FR-12 | Application decisions trigger status emails through Email Notifications and Email Service. | C4 Level 3 `uml/component.puml`; Deployment View `uml/deployment.puml` |
| NFR-03 | Request timing excludes time waiting for the external Email Service. | `docs/requirements.md`; `docs/architecture.md`; `uml/deployment.puml` |
| NFR-06 | Scheduled backend process uploads MySQL data daily to offsite Cloud Backup Storage configured for at least 30-day retention. | C4 Levels 1–3; Deployment View `uml/deployment.puml` |
| NFR-07 | Offsite backups and restore procedure support recovery within four hours of a declared incident. | Deployment View `uml/deployment.puml`; `docs/architecture.md` |
| NFR-10 | Replicated application server capacity is the logical deployment location for supporting at least 500 concurrent active users while meeting performance targets. | Deployment View `uml/deployment.puml` |
| NFR-12 | Application Server Node (xN) can scale horizontally as load grows. | Deployment View `uml/deployment.puml` |
| NFR-15 | HTTPS/TLS protects browser and external traffic; database storage is encrypted at rest; SQL connection is encrypted. | Deployment View `uml/deployment.puml` |
| NFR-16 | MySQL resides on a private network and allows SQL access only from the application backend; backend authorization remains enforced. | Deployment View `uml/deployment.puml`; C4 Level 3 `uml/component.puml` |
| NFR-21, NFR-30 | Browser node represents responsive client use and supported modern browsers. | Deployment View `uml/deployment.puml` |
| NFR-31 | Vendor-neutral application and database nodes plus portable configuration preserve host migration options. | Deployment View `uml/deployment.puml` |
| FR-02–FR-11, FR-13–FR-21 | Role-based React / Express / MySQL workflows remain mapped in the architecture. | `docs/requirements.md`; `docs/architecture.md`; C4 Levels 1–3 |
| NFR-01–NFR-02, NFR-04–NFR-05, NFR-08–NFR-09, NFR-11, NFR-13–NFR-14, NFR-17–NFR-20, NFR-22–NFR-29, NFR-32 | Existing performance, reliability, capacity, security, usability, maintainability, and compatibility constraints remain applicable. | `docs/requirements.md`; `docs/architecture.md` |

## External interfaces

- Email Service: registration/verification and application decision messages over SMTP/TLS or HTTPS; external wait excluded under NFR-03.
- Cloud Backup Storage: daily offsite MySQL backups over HTTPS, at least 30-day retention, and restoration support aligned with NFR-06/NFR-07.