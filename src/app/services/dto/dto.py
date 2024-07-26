from dataclasses import dataclass


@dataclass(frozen=True)
class RequestUserDto:
    username: str
    password: str


@dataclass(frozen=True)
class AuthenticationResponseDto:
    uid: int
    name: str



@dataclass(frozen=True)
class ResponseUserDto:
    uid: int
    username: str
    hashed_password: str
    urls: list["ResponseUrlDto"] | None

    @staticmethod
    def create(
        uid: int, username: str, hashed_password: str, urls: list["ResponseUrlDto"]
    ) -> "ResponseUserDto":
        return ResponseUserDto(
            uid=uid, username=username, hashed_password=hashed_password, urls=urls
        )


@dataclass(frozen=True)
class RequestUrlDto:
    url: str
    short_url: str

@dataclass(frozen=True)
class RequestLimitOffsetUrlDto:
    limit: int
    offset: int

@dataclass(frozen=True)
class RequestDeleteUrlDto:
    urlid: int


@dataclass(frozen=True)
class RequestInsertUrlDto:
    url: str


@dataclass
class RequestUpdateUrlDto:
    urlid: int
    url: str


@dataclass(frozen=True)
class ResponseUrlDto:
    urlid: int
    url: str
    short_url: str
    clics: int

    @staticmethod
    def create(urlid: int, url: str, short_url: str, clics: int) -> "ResponseUrlDto":
        return ResponseUrlDto(urlid=urlid, url=url, short_url=short_url, clics=clics)
