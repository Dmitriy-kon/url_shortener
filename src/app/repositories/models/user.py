from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.repositories.models.base import Base

if TYPE_CHECKING:
    from app.repositories.models.url import UrlDb

class UserDb(Base):
    __tablename__ = "users"

    uid: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', NOW())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', NOW())"),
        onupdate=text("TIMEZONE('utc', NOW())"),
    )

    urls: Mapped[list["UrlDb"]] = relationship("Url", back_populates="user")
