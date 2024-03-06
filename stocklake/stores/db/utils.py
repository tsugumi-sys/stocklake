# This code is highly inspired by https://github.com/mlflow/mlflow/blob/master/mlflow/server/auth/db/utils.py
from pathlib import Path

from alembic.command import upgrade
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy.engine.base import Engine


def _get_alembic_dir() -> Path:
    return Path(__file__).parent


def _get_alembic_config(url: str) -> Config:
    alembic_dir = _get_alembic_dir()
    alembic_ini_path = alembic_dir.parent / "alembic.ini"
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option(
        "script_location", str(alembic_dir.parent / "db_migrations")
    )
    url = url.replace("%", "%%")
    alembic_cfg.set_main_option("sqlalchemy.url", url)
    return alembic_cfg


def migrate(engine: Engine, revision: str) -> None:
    alembic_cfg = _get_alembic_config(engine.url.render_as_string(hide_password=False))
    with engine.begin() as conn:
        alembic_cfg.attributes["connection"] = conn
        upgrade(alembic_cfg, revision)


def migrate_if_needed(engine: Engine, revision: str) -> None:
    alembic_cfg = _get_alembic_config(engine.url.render_as_string(hide_password=False))
    script_dir = ScriptDirectory.from_config(alembic_cfg)
    with engine.begin() as conn:
        context = MigrationContext(conn)
        if context.get_current_revision() != script_dir.get_current_head():
            upgrade(alembic_cfg, revision)
