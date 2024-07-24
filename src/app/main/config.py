from dataclasses import dataclass, field
from os import getenv


@dataclass
class DatabaseConfig:
    db_uri: str

    @staticmethod
    def from_env() -> "DatabaseConfig":
        return DatabaseConfig(db_uri=getenv("DATABASE_URI", "sqlite:///app.db"))


@dataclass
class Config:
    db_config: DatabaseConfig = field(default_factory=lambda: DatabaseConfig.from_env())
