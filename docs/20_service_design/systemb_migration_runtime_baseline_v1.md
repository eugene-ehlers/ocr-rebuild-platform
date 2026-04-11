# System B Migration Runtime Baseline v1

## 1. Purpose

Define the governed, repeatable runtime baseline for System B migration execution and local migration validation.

This document exists so future migration execution packages do not rely on:
- ad hoc package installation in a warmed shell
- undocumented tool availability
- guesswork about how to provision Alembic/SQLAlchemy runtime support

This document is authoritative for the migration runtime baseline only.

---

## 2. Approved Stack

The approved System B migration/runtime stack is:

- PostgreSQL
- SQLAlchemy
- Alembic
- psycopg

This runtime baseline supports:
- migration execution
- migration revision inspection
- local disposable PostgreSQL validation
- schema and trigger validation packages

This document does not authorize:
- live/shared database use
- production migration execution
- schema redesign

---

## 3. Dependency Authority

The governed dependency declaration for the migration runtime is:

- `src/modules/persistence/requirements.txt`

That file is the single dependency authority for migration runtime provisioning.

Declared runtime packages:
- SQLAlchemy
- Alembic
- psycopg[binary]

No second conflicting dependency path is allowed for this migration runtime.

---

## 4. Repeatable Provisioning Baseline

The governed bootstrap mechanism is:

- `scripts/systemb/setup_migration_runtime.sh`

This script provisions a dedicated local virtual environment for migration work:

- default venv path: `.venv_systemb_migrations`

Provisioning steps:
1. create local virtual environment
2. activate it
3. install dependencies from `src/modules/persistence/requirements.txt`
4. verify Alembic is runnable

This makes the migration runtime reproducible without relying on warmed shell state.

---

## 5. Governed Execution Baseline

The governed helper for using the provisioned runtime is:

- `scripts/systemb/run_local_migration_validation.sh`

This helper:
- requires the governed migration venv to exist
- requires `SYSTEM_B_DATABASE_URL`
- runs Alembic from the governed runtime baseline

This script is a runtime entrypoint helper only.
It does not redefine schema or migrations.

---

## 6. Compliance Rules

Future migration validation packages must:

- provision the migration runtime using `scripts/systemb/setup_migration_runtime.sh`
- use dependencies from `src/modules/persistence/requirements.txt`
- avoid ad hoc `pip install` commands outside the governed bootstrap flow
- avoid reliance on pre-warmed shell state
- use only local/disposable PostgreSQL targets when the package requires local DB validation

Future migration validation packages must not:
- install random/untracked packages
- use shared/live database targets
- create a second migration runtime standard

---

## 7. Relationship to Other Authorities

This runtime baseline complements but does not replace:

- `docs/20_service_design/services_data_architecture_master_v1.md`
- `docs/20_service_design/services_oltp_data_architecture_v1.md`

Those documents define the data architecture and persistence design.
This document defines how the approved migration runtime is provisioned repeatably.

---

## 8. Out of Scope

This document does not define:
- schema design
- migration content
- ORM model content
- production deployment runtime
- business logic runtime

---

## 9. Next Use

The next local migration validation rerun package must:

1. provision runtime via `scripts/systemb/setup_migration_runtime.sh`
2. start a disposable local PostgreSQL container if approved
3. set `SYSTEM_B_DATABASE_URL`
4. execute Alembic and validation checks from the governed runtime
