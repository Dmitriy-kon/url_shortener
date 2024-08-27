import os
from dataclasses import dataclass, field


@dataclass
class DbTestSettings:
    db_test_url: str
    db_template_url: str

    db_test_name: str
    db_tamplate_name: str

    @staticmethod
    def from_env() -> "DbTestSettings":
        return DbTestSettings(
            db_test_url=os.getenv("DB_URI_TEST", "sqlite:///test.db"),
            db_template_url=os.getenv("DB_URI_TEMPLATE", "sqlite:///template.db"),
            db_test_name=os.getenv("POSTGRES_DB_TEST_NAME", "test_db"),
            db_tamplate_name=os.getenv("POSTGRES_DB", "template_db"),
        )


@dataclass
class SettingTest:
    db_config: DbTestSettings = field(default_factory=lambda: DbTestSettings.from_env())
