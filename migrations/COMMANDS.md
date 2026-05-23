# Alembic Migration Commands (Poetry)

This file is a practical command reference for database migrations in this project.

## Where to run

- Run commands from the project root:
  - `$HOME/workspaces/dev-python/projects/ai-taskflow`
- In your setup, run Poetry/Alembic inside distrobox.
- Keep PostgreSQL/Redis running from the host using Docker Compose.

## General command shape

- Default config (auto-loads `alembic.ini` from project root):
  - `poetry run alembic <command> [options]`
- Explicit config file (useful when running from a different folder):
  - `poetry run alembic -c alembic.ini <command> [options]`

## 1) Create a new migration (autogenerate)

- `poetry run alembic revision --autogenerate -m "<migration_name>"`
  - Generates a new migration file by diffing SQLAlchemy models vs database schema.

- `poetry run alembic -c alembic.ini revision --autogenerate -m "<migration_name>"`
  - Same as above, forcing the config file path explicitly.

Example:
- `poetry run alembic revision --autogenerate -m "create_tasks_table"`

## 2) Create an empty migration (manual script)

- `poetry run alembic revision -m "<migration_name>"`
  - Creates a blank migration file; you implement `upgrade()` and `downgrade()` manually.

## 3) Apply pending migrations (upgrade database)

- `poetry run alembic upgrade head`
  - Applies all pending migrations up to the latest revision.

- `poetry run alembic upgrade +1`
  - Applies one migration step forward from current revision.

- `poetry run alembic upgrade <revision_id_or_label>`
  - Upgrades to a specific target revision.

## 4) Check current migration state

- `poetry run alembic current`
  - Shows the current database revision.

- `poetry run alembic heads`
  - Shows latest revision(s) available in migration files.

- `poetry run alembic history`
  - Displays migration history.

- `poetry run alembic history --verbose`
  - Displays detailed migration history.

## 5) Roll back migrations (downgrade)

- `poetry run alembic downgrade -1`
  - Reverts one migration step.

- `poetry run alembic downgrade base`
  - Reverts all migrations back to an empty schema baseline.

- `poetry run alembic downgrade <revision_id_or_label>`
  - Reverts down to a specific target revision.

## 6) Validate if there are pending model changes

- `poetry run alembic check`
  - Fails if autogenerate would produce new operations (useful in CI).

## 7) Stamp revisions (without running SQL)

- `poetry run alembic stamp head`
  - Marks DB as current revision without applying migration SQL.

- `poetry run alembic stamp base`
  - Marks DB as base revision without applying downgrade SQL.

- `poetry run alembic stamp <revision_id_or_label>`
  - Sets migration marker to a specific revision only.

## 8) Generate SQL scripts instead of applying directly

- `poetry run alembic upgrade head --sql > migrations/full_upgrade.sql`
  - Generates SQL script for full upgrade to latest revision.

- `poetry run alembic downgrade base --sql > migrations/full_downgrade.sql`
  - Generates SQL script for full rollback to base.

- `poetry run alembic upgrade <target_revision> --sql > migrations/upgrade_to_target.sql`
  - Generates SQL script for upgrade to a specific revision.

- `poetry run alembic downgrade <target_revision> --sql > migrations/downgrade_to_target.sql`
  - Generates SQL script for downgrade to a specific revision.

## 9) Branch handling (advanced)

- `poetry run alembic branches`
  - Shows branch points in migration graph.

- `poetry run alembic merge -m "<merge_name>" <rev1> <rev2>`
  - Creates a merge migration when multiple heads exist.

## 10) Edit generated migration file quickly

- `poetry run alembic edit <revision_id>`
  - Opens the migration file in your configured editor.

## Useful project workflow

1. Ensure database is running:
   - `docker compose up -d`
2. Create migration:
   - `poetry run alembic revision --autogenerate -m "<migration_name>"`
3. Review generated file under `migrations/versions/`.
4. Apply migration:
   - `poetry run alembic upgrade head`
5. Verify state:
   - `poetry run alembic current`

## EF Core mental mapping (for quick transition)

- Add-Migration -> `alembic revision --autogenerate -m "..."`
- Update-Database -> `alembic upgrade head`
- Update-Database 0 -> `alembic downgrade base`
- Update-Database <migration> -> `alembic upgrade <revision>`
- Script-Migration -> `alembic upgrade ... --sql` or `alembic downgrade ... --sql`
- Remove-Migration (last, not applied) -> delete latest file in `migrations/versions/` carefully

## Important notes

- Alembic does not have a direct `remove migration` command like EF Core.
- If the latest migration was not applied, you can delete the newest file manually.
- If it was applied, run a downgrade first, then remove or replace the migration file.
- Keep `.env` credentials aligned with `docker-compose.yml` credentials.
