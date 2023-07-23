"""SQLAlchemy session management."""

from sqlite3 import Connection

from sqlalchemy import create_engine, event
from sqlalchemy.dialects.sqlite import dialect as sqlite_dialect
from sqlalchemy.orm import sessionmaker

from product_rater.config import config


def _fk_pragma_on_connect(dbapi_con: Connection, *_):
    """Enable the foreign keys in SQLite."""
    dbapi_con.execute("pragma foreign_keys=ON")


engine = create_engine(config.DB_URI)
"""SQLAlchemy engine."""

if isinstance(engine.dialect, sqlite_dialect):
    """Activate foreign keys behavior in SQLite."""
    event.listen(engine, "connect", _fk_pragma_on_connect)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
""""SQLAlchemy session local class."""
