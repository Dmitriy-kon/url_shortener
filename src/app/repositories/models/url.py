from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.repositories.models.base import Base

if TYPE_CHECKING:
    from app.repositories.models.user import UserDb


class UrlDb(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    short_url: Mapped[str]
    clics: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', NOW())")
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.uid"))
    user: Mapped["UserDb"] = relationship("User", back_populates="urls")
