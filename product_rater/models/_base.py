"""Base class for SQLAlchemy models."""

from sqlalchemy.ext.declarative import declarative_base, declared_attr


class _Base:
    """Base class for SQLAlchemy models."""

    @declared_attr
    def __tablename__(cls):
        """Return the table name for the model."""
        return cls.__name__.lower()


Base = declarative_base(cls=_Base)
