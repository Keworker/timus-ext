from typing import Callable

import sqlalchemy as orm
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

SqlAlchemyBase = orm.declarative_base()

# noinspection PyTypeChecker
__factory: Callable[[], Session] = None


def global_init(db_file):  # {
    """
    Initialize the database for app API.
    :param db_file: path to database file
    :return: Unit
    """
    global __factory
    if __factory:  # {
        return
    # }
    if not db_file or not db_file.strip():  # {
        raise FileNotFoundError("Invalid database file.")
    # }
    conn_str = f"sqlite:///{db_file.strip()}?check_same_thread=False"
    engine = orm.create_engine(conn_str, echo=False)
    if not (database_exists(engine.url)):  # {
        create_database(engine.url)
    # }
    __factory = orm.sessionmaker(bind=engine)
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from database import __all_models
    SqlAlchemyBase.metadata.create_all(engine)
# }


def create_session() -> Session:  # {
    """
    Create new session for database connection.
    :return: Session
    """
    global __factory
    return __factory()
# }
