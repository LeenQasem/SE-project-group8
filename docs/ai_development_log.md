# AI Development Log

This log records AI-assisted engineering activities across each increment of the **Event & Volunteer Management System** in accordance with Section 3.3 of the project guidelines. Full task prompts are stored in the [`prompts/`](../prompts/) directory; minor interactive exchanges are summarized rather than logged verbatim.

## Increment Log

| Version | Agent | Task / Prompt Ref. | Changed Modules | Issues / Corrections | Student Review |
|---|---|---|---|---|---|
| `v0.1.0-design` | OpenAI Codex | [Increment 1 architecture and UML prompt](../prompts/v0.1.0-design_increment1_architecture_uml.md) | `uml/use_case.puml`, `uml/class_diagram.puml`, `uml/sequence-diagrams/SD01_High_Level_UC01_Auth.puml`–`SD04_Low_Level_UC02_UserManagement.puml`, `uml/activity-diagrams/AD_Increment1_Combined.puml`, `uml/erd_increment1.puml`, `docs/incremental_development_plan.md`, `docs/traceability_matrix.md` | Reduced the class model to `AuthController`, `AdminUserController`, `User`, and `UserRole`; scoped design to UC01/UC02; recorded Volunteer-default registration and guarded manual initial Administrator provisioning. ERD and combined activity sources were rendered and validated. No application code or automated tests were implemented or run. | Pending student review |
| `v0.1.0` | Codex | [Role Management & RBAC prompt record](../prompts/v0.1.0-role-management-rbac.md) | `src/backend/rbac.py`, `src/backend/bootstrap_admin.py`, `src/backend/user_management_service.py`, `src/backend/test_rbac.py`, `src/backend/test_user_management_service.py` | 46 unit/service tests passed (`unittest discover -s src/backend -p "test_*.py" -v`; 1.455s, `OK`). | Pending student review |
| `v0.1.0` | Planned | Planned prompt: `prompts/v0.1.0-task.md` | Planned: `AuthController`, `AdminUserController`, `User`, `UserRole`, `tests/auth/`, `tests/admin/` | Pending implementation | Pending review |
| `v0.2.0-design` | Planned | Planned prompt: `prompts/v0.2.0-design-task.md` | Planned: `uml/increment2/`, `docs/incremental_development_plan.md`, `docs/traceability_matrix.md` | Pending design | Pending review |
| `v0.2.0` | Planned | Planned prompt: `prompts/v0.2.0-task.md` | Planned: Event and Explore modules, `tests/events/`, `tests/explore/` | Pending implementation | Pending review |
| `v0.3.0-design` | Planned | Planned prompt: `prompts/v0.3.0-design-task.md` | Planned: `uml/increment3/`, `docs/incremental_development_plan.md`, `docs/traceability_matrix.md` | Pending design | Pending review |
| `v0.3.0` | Planned | Planned prompt: `prompts/v0.3.0-task.md` | Planned: Application and Attendance modules, `tests/applications/`, `tests/attendance/` | Pending implementation | Pending review |
| `v0.4.0-design` | Planned | Planned prompt: `prompts/v0.4.0-design-task.md` | Planned: `uml/increment4/`, `docs/incremental_development_plan.md`, `docs/traceability_matrix.md` | Pending design | Pending review |
| `v0.4.0` | Planned | Planned prompt: `prompts/v0.4.0-task.md` | Planned: Analytics module, `tests/analytics/` | Pending implementation | Pending review |
| `v1.0.0` | Planned | Planned prompt: `prompts/v1.0.0-task.md` | Planned: integrated system and `tests/e2e/` | Pending final integration | Pending review |

