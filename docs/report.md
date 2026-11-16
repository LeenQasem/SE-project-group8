# Report

## Project progress

The architecture documents the three-tier React frontend, Node.js/Express backend, and MySQL database, including the Volunteer, Event Organizer, and Administrator actors and integrations with Email Service and Cloud Backup Storage.

A vendor-neutral C4 Deployment View now shows the client browser, horizontally scalable application server, private database server, and external email and backup infrastructure. It links the topology to browser compatibility and responsiveness, TLS, backend-only database access, horizontal scaling, daily offsite backup with 30-day retention, four-hour recovery support, and deployment portability (NFR-06, NFR-07, NFR-10, NFR-12, NFR-15, NFR-16, NFR-21, NFR-30, NFR-31).

PlantUML sources are in `uml/`; rendered PNGs are in `uml/rendered/`. Requirement mappings are in `docs/traceability_matrix.md`. These are logical design artifacts; provider selection, sizing, configuration, implementation, and recovery verification remain future work.