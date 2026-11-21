# Testing

# Increment 1 Test Plan

The checkout currently contains no application code, dependency manifest, or test framework. The following are required automated test cases for implementation; they are specifications, not evidence that tests have run. Select the runner when the application scaffold is established.

| Test | Expected result |
|---|---|
| Valid public registration | Creates one user with unique email, `VOLUNTEER` role, active status, and salted password hash; plaintext password is absent from persistence/logs. |
| Client submits `ADMINISTRATOR` or `EVENT_ORGANIZER` during public signup | Role field is ignored or rejected; persisted role is always `VOLUNTEER`. |
| Invalid name/email/password or duplicate email | Registration is rejected with safe field-level feedback; no user/session row is created. |
| Valid login | Correct hash verification creates a persisted session with token hash and expiry; identity and role are returned. |
| Invalid password, unknown email, inactive account, expired/revoked session | Authentication is rejected without revealing whether an account exists or exposing internal errors. |
| Logout | Session is revoked; subsequent validation fails. |
| Protected operation without valid session | Backend denies access. |
| Non-administrator attempts list/view/update/role assignment | Backend denies access and writes an audit event. |
| Administrator updates permitted account fields or role | Valid data and one of the three roles are persisted; audit event is written. |
| Initial administrator setup with valid one-time secret and no administrator | Creates exactly one administrator transactionally and consumes authorization. |
| Initial administrator setup with invalid/reused secret or existing administrator | Fails without creating another privileged account; concurrent attempts cannot create multiple administrators. |
| Input injection / malformed payload checks | Inputs are validated/sanitized; database operations remain parameterized. |

NFR-01 login latency, NFR-11 transport/storage protection, NFR-14 audit coverage, and NFR-20 secret-free logs require integration/deployment verification in addition to unit tests.
