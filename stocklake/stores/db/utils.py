# This code is highly inspired by https://github.com/mlflow/mlflow/blob/master/mlflow/server/auth/db/utils.py
from pathlib import Path

from alembic.command import revision, upgrade
from alembic.config import Config
from alembic.runtime.environment import EnvironmentContext
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


def autogenerate_revision(engine: Engine, message: str):
    alembic_cfg = _get_alembic_config(engine.url.render_as_string(hide_password=False))
    alembic_script_dir = ScriptDirectory.from_config(alembic_cfg)

    def process_revision_directives(context, revision, directives):
        if directives[0].upgrade_ops.is_empty():
            directives[:] = []
        else:
            script = directives[0]
            script.rev_id = alembic_script_dir.generate_revision_id()

    print(alembic_script_dir.get_revisions("heads"))
    print(alembic_script_dir.get_revisions("head"))
    print(
        set(alembic_script_dir.get_revisions("heads"))
        != set(alembic_script_dir.get_revisions("head"))
    )

    with EnvironmentContext(
        alembic_cfg,
        alembic_script_dir,
        fn=process_revision_directives,
        as_sql=False,
        starting_rev=None,
        destination_rev="head",
        tag=None,
    ):
        revision(alembic_cfg, message, autogenerate=True)
