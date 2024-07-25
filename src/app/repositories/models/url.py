from datetime import datetime
from typing import TYPE_CHECKING, cast

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.repositories.models.base import Base
from app.services.dto.dto import ResponseUrlDto

if TYPE_CHECKING:
    from app.repositories.models.user import UserDb


class UrlDb(Base):
    __tablename__ = "urls"

    urlid: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(nullable=False)
    short_url: Mapped[str] = mapped_column(nullable=False)
    clics: Mapped[int] = mapped_column(default=0)

    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', NOW())")
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.uid"))
    user: Mapped["UserDb"] = relationship("UserDb", back_populates="us_urls")

    def to_dto(self) -> ResponseUrlDto:
        return ResponseUrlDto(
            urlid=cast(int, self.urlid),
            url=cast(str, self.url),
            short_url=cast(str, self.short_url),
            clics=cast(int, self.clics),
        )
