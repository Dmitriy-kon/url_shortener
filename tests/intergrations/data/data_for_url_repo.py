from contextlib import nullcontext as not_raise

import pytest
from sqlalchemy.exc import IntegrityError

data_for_insert_test = [
    ("test_user1", "testpassword", "https://example.com", "asdasSSH@", not_raise()),
    (
        "test_user2",
        "testpassword2",
        "https://another-example.com",
        "ZH^YHSAGHD*@HS",
        not_raise(),
    ),
    (
        "test_user3",
        "testpassword3",
        "https://yet-another-example.com",
        "short1",
        not_raise(),
    ),
    (
        "test_user4",
        "testpassword4",
        "https://yet-another-example.com",
        "short1",
        pytest.raises(IntegrityError),
    ),
    (
        "test_user5",
        "testpassword5",
        None,
        "asdasdzxc645",
        pytest.raises(IntegrityError),
    ),
    (
        "test_user6",
        "testpassword6",
        "https://yet-another-example.com",
        None,
        pytest.raises(IntegrityError),
    ),
]
