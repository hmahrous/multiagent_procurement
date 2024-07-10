import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import get_settings


def create_database_if_not_exists():
    """
    Function to create database if not exists. This function creates a new synchronous connection with
    default database and creates the application specific database
    """

    engine = create_engine(
        get_settings().sqlalchemy_sync_default_database_uri.render_as_string(
            hide_password=False
        )
    )
    autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT")
    default_db_session = sessionmaker(autoflush=False, bind=autocommit_engine)
    db = default_db_session()
    database_exists = check_if_application_database_exists(db)

    if database_exists:
        return

    print("Database doesn't exist. Creating database ")
    db.execute(text(f'CREATE DATABASE "{get_settings().database.db}"'))
    print("Database created ")
    default_db_session.close_all()
    return


def check_if_application_database_exists(db):
    result = db.execute(
        text(
            f"SELECT 1 FROM pg_database WHERE datname = '{get_settings().database.db}'"
        )
    ).all()
    return bool(len(result))


if __name__ == "__main__":
    create_database_if_not_exists()
