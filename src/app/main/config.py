from dataclasses import dataclass, field
from os import getenv


@dataclass
class DatabaseConfig:
    db_uri: str

    @staticmethod
    def from_env() -> "DatabaseConfig":
        return DatabaseConfig(db_uri=getenv("DB_URI", "None"))


@dataclass
class JwtConfig:
    secret_key: str
    expire: int = field(default=5)
    algorithm: str = field(default="HS256")

    @staticmethod
    def from_env() -> "JwtConfig":
        return JwtConfig(
            secret_key=getenv("SECRET_KEY", "None"),
            expire=int(getenv("EXPIRE", "5")),
            algorithm=getenv("ALGORITHM", "HS256"),
        )


@dataclass
class Config:
    db_config: DatabaseConfig = field(default_factory=lambda: DatabaseConfig.from_env())
    jwt_config: JwtConfig = field(default_factory=lambda: JwtConfig.from_env())
