# This code is highly inspired by https://github.com/mlflow/mlflow/blob/master/mlflow/server/auth/db/utils.py
import os
import shutil
from pathlib import Path

from alembic.command import revision, upgrade
from alembic.config import Config
from sqlalchemy.engine.base import Engine

from stocklake.core.constants import _MOCK_ALEMBIC_SCRIPT_LOCATION
from stocklake.environment_variables import _STOCKLAKE_ENVIRONMENT


def _get_alembic_dir() -> Path:
    return Path(__file__).parent


def _get_alembic_config(url: str) -> Config:
    alembic_dir = _get_alembic_dir()
    alembic_ini_path = alembic_dir.parent / "alembic.ini"
    alembic_cfg = Config(alembic_ini_path)
    script_location = str(alembic_dir.parent / "db_migrations")
    if _STOCKLAKE_ENVIRONMENT.get() == "test":
        os.makedirs(_MOCK_ALEMBIC_SCRIPT_LOCATION, exist_ok=True)
        os.makedirs(
            os.path.join(_MOCK_ALEMBIC_SCRIPT_LOCATION, "versions"), exist_ok=True
        )
        for filename in ["env.py", "script.py.mako"]:
            shutil.copy(
                os.path.join(script_location, filename),
                os.path.join(_MOCK_ALEMBIC_SCRIPT_LOCATION, filename),
            )
        script_location = _MOCK_ALEMBIC_SCRIPT_LOCATION
    alembic_cfg.set_main_option("script_location", script_location)

    url = url.replace("%", "%%")
    alembic_cfg.set_main_option("sqlalchemy.url", url)
    return alembic_cfg


def migrate(engine: Engine, revision: str) -> None:
    alembic_cfg = _get_alembic_config(engine.url.render_as_string(hide_password=False))
    with engine.begin() as conn:
        alembic_cfg.attributes["connection"] = conn
        upgrade(alembic_cfg, revision)


def autogenerate_revision(engine: Engine, message: str):
    revision(
        _get_alembic_config(engine.url.render_as_string(hide_password=False)),
        message,
        autogenerate=True,
    )
