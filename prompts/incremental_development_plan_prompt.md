# Master Prompt: Incremental Development Plan

## Objective

Prepare or revise `docs/incremental_development_plan.md` for the Event & Volunteer Management System. The plan must translate the requirements already documented in this repository into clear, reviewable increments and release checkpoints. Do not create additional prompt files.

## Role

Act as a careful software project planner. Use precise, professional language and preserve the project's terminology, established decisions, and documentation style. 

## Authoritative sources

1. `docs/requirements.md` is the authority for all functional and non-functional requirements, their identifiers, and their wording.
2. `README.md`, `docs/project_description.md`, `docs/architecture.md`, and existing UML/database artifacts provide project context and established design decisions.
3. The user-provided development approach defines the intended increments, version checkpoints, deliverables, and release process where these do not conflict with `docs/requirements.md`.

If a source conflicts with `docs/requirements.md`, preserve the requirement as written and clearly identify the conflict for review. Do not silently renumber or rewrite requirements.

## Planning rules

- Map each increment to the correct functional requirement identifiers:
  - Authentication and User Management: FR-01–FR-04 and FR-20.
  - Event Management and Discovery: FR-05–FR-09.
  - Volunteer Applications and Assignments: FR-10–FR-15.
  - Attendance, Hours Tracking and Reports: FR-16–FR-19 and FR-21.
- Reference applicable non-functional requirements using the identifiers exactly as they appear in `docs/requirements.md`. The source currently labels the 500-concurrent-user requirement as `NFR-6: NFR-10`; do not confuse it with the separate password-hashing requirement labeled `NFR-10`.
- Distinguish required behavior from design proposals. Where a requirement leaves a policy or implementation choice open, mark it as a decision for team review instead of presenting it as a requirement.
- Do not add unsupported features or acceptance criteria. In particular, do not assume dashboards, duplicate-account rules, duplicate-application rules, or other behavior unless it is supported by a requirement or explicitly requested in the development approach.
- Keep each design checkpoint focused on requirements analysis, workflows, architecture/data design, deliverables, and review criteria. Keep each working checkpoint focused on implementing the approved design, validating relevant requirements, and documenting evidence.
- Include all applicable cross-cutting non-functional requirements in the integration/release checkpoint. Do not imply that a requirement is satisfied without implementation or validation evidence.

## Required plan structure

1. **Development approach:** explain the incremental method and the design and working checkpoints.
2. **Increment summary:** provide a table with version, checkpoint type, capability, deliverables/evidence, and accurate requirement links.
3. **Detailed increment specifications:** for each of the four increments, include:
   - version pair (`-design` and working version);
   - objective and main question;
   - design checkpoint scope, tools, deliverables, and acceptance criteria;
   - working checkpoint scope, tools, deliverables, and acceptance criteria.
4. **Final integration and release:** define v1.0.0 activities, evidence, and acceptance criteria covering the full system and applicable functional and non-functional requirements.
5. **Development and version-control process:** describe review, implementation, testing, pull-request, merge, tagging, traceability, and documentation steps without claiming these actions have occurred.
6. **Final release statement:** define what v1.0.0 represents.

## Quality review before saving

- Verify every functional requirement from FR-01 through FR-21 is covered by an increment or final integration.
- Verify requirement identifiers and descriptions against `docs/requirements.md`; do not copy inaccurate mappings from an older plan.
- Verify that role permissions, event ownership, capacity, application decisions, assignments, attendance, hours, and reports appear only where supported by the requirements and agreed project scope.
- Verify non-functional concerns such as security, data integrity, scalability, accessibility, testing, documentation, portability, and time zones are assigned to relevant checkpoints or final integration.
- Check that design decisions left open by the requirements are identified for review.
- Keep the plan internally consistent and avoid claiming approval, implementation, testing, merging, or release before evidence exists.

## Output

Save the completed plan to `docs/incremental_development_plan.md`. In your completion summary, state the file changed, the requirement-mapping review performed, any unresolved conflicts or decisions, and validation performed. Do not create or modify other files unless explicitly requested.