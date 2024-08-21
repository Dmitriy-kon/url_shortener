from contextlib import nullcontext as not_raise

import pytest
from pydantic import ValidationError
from src.app.routes.schemas.urls import SUrlIn


class TestUrlValidate:
    @pytest.mark.parametrize(
        ("url", "exception"),
        [
            ("http://www.google.com", not_raise()),
            ("https://www.yahoo.com", not_raise()),
            ("www.google.com", pytest.raises(ValidationError)),
            ("some_data", pytest.raises(ValidationError)),
            ("ya.ru", pytest.raises(ValidationError)),
        ],
    )
    def test_url_validate(self, url, exception) -> None:
        with exception:
            SUrlIn.model_validate_strings({"url": url})
