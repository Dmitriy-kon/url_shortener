from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for orm models."""

    __abstract__ = True
