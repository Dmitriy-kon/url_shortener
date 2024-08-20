from datetime import datetime
from typing import TYPE_CHECKING, cast

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.repositories.models.base import Base
from app.services.dto.dto import ResponseUrlDto, ResponseUserDto

if TYPE_CHECKING:
    from app.repositories.models.url import UrlDb


class UserDb(Base):
    __tablename__ = "users"

    uid: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', NOW())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', NOW())"),
        onupdate=text("TIMEZONE('utc', NOW())"),
    )

    us_urls: Mapped[list["UrlDb"]] = relationship("UrlDb", back_populates="user")

    def to_dto(self) -> ResponseUserDto:
        return ResponseUserDto.create(
            uid=cast(int, self.uid),
            username=cast(str, self.username),
            hashed_password=cast(str, self.hashed_password),
            urls=cast(list["ResponseUrlDto"], [url.to_dto() for url in self.us_urls]),
        )
